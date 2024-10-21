from app.celery_app import app
from app.database import engine
from sqlmodel import Session
import logging
from dotenv import load_dotenv
import asyncio
from app.repositories.message_repository import MessageRepository
from app.services.thirdparty_ai_service import ThirdPartyAIService
import json
from sqlalchemy.orm import sessionmaker

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.task
def chat_task(msg, ai_model="openai", temperature=0.7):
    async def async_chat():
        logger.info(f"chat: {msg}")
        try:
            with SessionLocal() as session:
                message_repository = MessageRepository(session)
                thirdparty_ai_service = ThirdPartyAIService(message_repository)
                response = await thirdparty_ai_service.chat(ai_model, msg, temperature)
                #response_dict = json.loads(response)
                return response['message']
        except Exception as e:
            logger.error(f"Error in chat_task: {str(e)}")
            return json.dumps({"error": str(e)})

    return asyncio.run(async_chat())
