from app.celery_app import app
from app.database import engine
from sqlmodel import Session
from typing import Dict
import logging
from dotenv import load_dotenv
import asyncio
from app.repositories.message_repository import MessageRepository
from app.services.thirdparty_ai_service import ThirdPartyAIService, EmbeddingService
from app.task_models.msg_info import MsgInfo
import json

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task
def request_bot_msg_task(ai_model="openai", temperature=0.7) -> MsgInfo:
    async def async_chat():
        try:
            with Session(engine) as session:
                message_repository = MessageRepository(session)
                thirdparty_ai_service = ThirdPartyAIService(message_repository)
                
                response = await thirdparty_ai_service.chat(ai_model, temperature)

                embedding_service = EmbeddingService(message_repository)
                await embedding_service.create_msg_embedding(response.text, response.id)

                return MsgInfo(msg=response.text, msg_id=response.id)
        except Exception as e:
            logger.error(f"Error in request_bot_msg_task: {str(e)}")
            return json.dumps({"error": str(e)})

    return asyncio.run(async_chat())
