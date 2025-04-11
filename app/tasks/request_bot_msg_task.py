from app.celery_app import app
from app.database import engine
from sqlmodel import Session
from typing import Dict
import logging
from dotenv import load_dotenv
import asyncio
import redis
import os
from app.repositories.chat_repository import ChatRepository
from app.repositories.user_repository import UserRepository
from app.requests.thirdparty_ai_request import ThirdPartyAIRequest, EmbeddingRequest, PromptContext
from app.models.attendee import AttendeeType
from app.task_models.msg_info import MsgInfo
import app.prompts as prompts
from app.helpers.prompt_builder import build_prompt
import json


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

@app.task
def request_bot_msg_task(chatroom_id: int, temperature=0.7) -> MsgInfo:
    async def async_chat():
        try:
            with Session(engine) as session:
                user_repository = UserRepository(session)
                chat_repository = ChatRepository(session)

                recent_messages = chat_repository.get_latest_messages(chatroom_id, 10)
                logger.info(f"recent_messages: {recent_messages.reverse()}")

                user_attendee = chat_repository.get_attendees_by_chatroom_id(chatroom_id, AttendeeType.user)[0]
                user_persona = chat_repository.get_user_persona_by_attendee_id(user_attendee.id)
                #user_name_with_attendee_id = user_persona.nickname + "(attendee_id: " + str(user_attendee.id) + ")"
                user_name_with_attendee_id = user_persona.nickname
                
                persona_list = []
                bot_attendees = chat_repository.get_attendees_by_chatroom_id(chatroom_id, AttendeeType.bot)
                for ba in bot_attendees:
                    bot_persona = user_repository.get_bot_by_attendee_id(ba.id)
                    logger.info(f"bot_persona: {bot_persona.name}")
                    logger.info(f"bot_persona.property: {bot_persona.property}")
                    #persona_list.append(bot_persona.name + "(attendee_id: " + str(ba.id) + ")" + "\n" + bot_persona.property["persona"])
                    persona_list.append(bot_persona.name + "\n" + bot_persona.property["persona"])

                prompt_context = PromptContext()
                prompt_context.prompt_template = build_prompt(
                    template=prompts.prompt_template,
                    user_name=user_name_with_attendee_id,
                    user_description=user_persona.description,
                    user_age=user_persona.age,
                    user_gender="남성" if user_persona.gender == "male" else "여성" if user_persona.gender == "female" else "non-binary",
                    persona_list=persona_list,
                    persona_relationship=[]
                )
                logger.info(f"prompt: {prompt_context.prompt_template}")

                ai_model = "gemini-2.0-flash-001" #bot.ai_model

                ai_request = ThirdPartyAIRequest(prompt_context)
                ai_msg = await ai_request.chat(recent_messages, ai_model, temperature)

                # embedding_request = EmbeddingRequest(chat_repository)
                # await embedding_request.create_msg_embedding(ai_msg, ai_msg.id)

                message = chat_repository.create_message(ai_msg, chatroom_id, bot_attendees[0].id, AttendeeType.bot)
                session.commit()

                # web 서버로 메시지 전송 (web 서버가 클라이언트에게 전달함)
                redis_client.publish("chat_messages", json.dumps({"chatroom_id": chatroom_id, "sender_id": bot_attendees[0].id, "message": message.text}))

                return MsgInfo(msg=message.text, msg_id=message.id)
        except Exception as e:
            logger.error(f"Error in request_bot_msg_task: {str(e)}")
            return json.dumps({"error": str(e)})

    return asyncio.run(async_chat())
