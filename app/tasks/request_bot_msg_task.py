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
import json

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

@app.task
def request_bot_msg_task(chatroom_id: int, bot_attendee_id: int, temperature=0.7) -> MsgInfo:
    async def async_chat():
        try:
            with Session(engine) as session:
                user_repository = UserRepository(session)
                chat_repository = ChatRepository(session)

                bot = user_repository.get_bot_by_attendee_id(bot_attendee_id)
                ai_model = bot.ai_model
                logger.info(f"bot name: {bot.name}")
                logger.info(f"ai_model: {ai_model}")

                recent_messages = chat_repository.get_latest_messages(chatroom_id, 10)
                logger.info(f"recent_messages: {recent_messages.reverse()}")

                prompt_context = PromptContext()
                #prompt_context.prompt_template = bot.property["prompt"]
                logger.info(f"prompt_context: {prompt_context.prompt_template}")

                ai_request = ThirdPartyAIRequest(prompt_context)
                ai_msg = await ai_request.chat(recent_messages, ai_model, temperature)

                # embedding_request = EmbeddingRequest(chat_repository)
                # await embedding_request.create_msg_embedding(ai_msg, ai_msg.id)

                message = chat_repository.create_message(ai_msg, chatroom_id, bot_attendee_id, AttendeeType.bot)
                session.commit()

                # web 서버로 메시지 전송 (web 서버가 클라이언트에게 전달함)
                redis_client.publish("chat_messages", json.dumps({"chatroom_id": chatroom_id, "sender_id": bot_attendee_id, "message": message.text}))

                return MsgInfo(msg=message.text, msg_id=message.id)
        except Exception as e:
            logger.error(f"Error in request_bot_msg_task: {str(e)}")
            return json.dumps({"error": str(e)})

    return asyncio.run(async_chat())
