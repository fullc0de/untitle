from app.celery_app import app
from app.database import engine
from sqlmodel import Session
import logging
from dotenv import load_dotenv
import asyncio
from app.repositories.message_repository import MessageRepository
from app.services.thirdparty_ai_service import EmbeddingService
from app.task_models.msg_info import MsgInfo
from typing import List

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task
def msg_embedding_task(msgs: List[MsgInfo]):
    async def async_task():
        for i, msg in enumerate(msgs):
            logger.info(f"msg[{i}]: {msg}") 

        try:
            with Session(engine) as session:
                logger.info(f"session: {session}")
                message_repository = MessageRepository(session)
                service = EmbeddingService(message_repository)
                #await asyncio.gather(*[service.create_msg_embedding(msg.msg, msg.msg_id) for msg in msgs])
                await service.create_msg_embedding_batch([(msg.msg_id, msg.msg) for msg in msgs])
        except Exception as e:
            logger.error(f"Error in chat_embedding_task: {str(e)}")

    return asyncio.run(async_task())