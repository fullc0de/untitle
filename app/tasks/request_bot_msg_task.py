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
from app.services.thirdparty_ai_service import ThirdPartyAIService, EmbeddingService
from app.task_models.msg_info import MsgInfo
import json

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

@app.task
def request_bot_msg_task(ai_model="openai", temperature=0.7) -> MsgInfo:
    async def async_chat():
        try:
            with Session(engine) as session:
                chat_repository = ChatRepository(session)
                thirdparty_ai_service = ThirdPartyAIService(chat_repository)

                response = await thirdparty_ai_service.chat(ai_model, temperature)

                # web 서버로 메시지 전송 (web 서버가 클라이언트에게 전달함)
                redis_client.publish("chat_messages", json.dumps({"message": response.text}))

                embedding_service = EmbeddingService(chat_repository)
                await embedding_service.create_msg_embedding(response.text, response.id)

                return MsgInfo(msg=response.text, msg_id=response.id)
        except Exception as e:
            logger.error(f"Error in request_bot_msg_task: {str(e)}")
            return json.dumps({"error": str(e)})

    return asyncio.run(async_chat())
