from fastapi import APIRouter, Query, Depends
from fastapi.responses import FileResponse
from app.tasks.chat_task import chat_task
from app.tasks.msg_embedding_task import msg_embedding_task
from app.repositories.message_repository import MessageRepository
from sqlmodel import Session
from app.database import get_session
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/chat")
def chat(msg: str = Query(..., description="empty message")):
    task = chat_task.delay(msg, "openai", 0.7)
    try:
        reply = task.get(timeout=10)
        logger.info(f"Task result: {reply}")
        msg_embedding_task.delay([reply['user'], reply['bot']])
        return {"reply": reply['bot'].msg}
    except TimeoutError:
        return {"status": "PENDING", "message": "작업이 아직 완료되지 않았습니다. 나중에 다시 시도해주세요."}



@router.get("/chat-test")
async def chat_test():
    logger.info("chat_test")
    return FileResponse("app/static/chat.html", media_type="text/html")


@router.get("/messages")
def get_messages(session: Session = Depends(get_session)):
        message_repository = MessageRepository(session)
        messages = message_repository.get_all_messages()
        return [{"sender": "사용자" if msg.sender_type == "user" else "서버", "text": msg.text} for msg in messages]
