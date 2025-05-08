from app.celery_app import app
from app.database import engine
from sqlmodel import Session
from typing import Dict
import logging
from dotenv import load_dotenv
import asyncio
import redis
import os
from app.models.chat import SenderType
from app.repositories.chat_repository import ChatRepository
from app.requests.thirdparty_ai_request import ThirdPartyAIRequest, PromptContext
from app.task_models.msg_info import MsgInfo
import app.prompts as prompts
# from app.helpers.prompt_builder import build_prompt
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
                chat_repository = ChatRepository(session)

                bot = chat_repository.get_bot_by_chatroom_id(chatroom_id)
                recent_messages = chat_repository.get_latest_messages(chatroom_id, 10)
                logger.info(f"recent_messages: {recent_messages.reverse()}")

                prompt_context = PromptContext()
                prompt_context.prompt_template = prompts.prompt_unknown_template_2
                logger.info(f"prompt: {prompt_context.prompt_template}")

                ai_model = "openrouter"

                ai_request = ThirdPartyAIRequest(prompt_context)
                ai_msg = await ai_request.chat(recent_messages, ai_model, temperature)
                logger.info(f"Bot 메시지: {ai_msg}")
                content = {
                    "text": ai_msg
                }
                message = chat_repository.create_chat(content, chatroom_id, bot.id, SenderType.bot)
                session.commit()

                # web 서버로 메시지 전송 (web 서버가 클라이언트에게 전달함)
                redis_client.publish("chat_messages", json.dumps({"chatroom_id": chatroom_id, "sender_id": bot.id, "message": message.text}))

                return MsgInfo(msg=ai_msg, msg_id=message.id)
        except Exception as e:
            logger.error(f"Error in request_bot_msg_task: {str(e)}")
            return json.dumps({"error": str(e)})

    return asyncio.run(async_chat())
