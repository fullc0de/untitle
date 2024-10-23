from app.celery_app import app
from app.database import engine
from sqlmodel import Session
import logging
from dotenv import load_dotenv
import asyncio
from app.repositories.message_repository import MessageRepository
from app.services.thirdparty_ai_service import EmbeddingService
import json

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task
def chat_embedding_task(msg):
    async def async_chat():
        logger.info(f"chat: {msg}")
        try:
            with Session(engine) as session:
                logger.info(f"session: {session}")
                message_repository = MessageRepository(session)
                thirdparty_ai_service = EmbeddingService()
                response = await thirdparty_ai_service.chat(ai_model, msg, temperature)
                #response_dict = json.loads(response)
                return response['message']
        except Exception as e:
            logger.error(f"Error in chat_task: {str(e)}")
            return json.dumps({"error": str(e)})

    return asyncio.run(async_chat())