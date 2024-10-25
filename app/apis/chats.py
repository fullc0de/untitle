from fastapi import APIRouter, Query, Body, Depends, HTTPException
from fastapi.responses import FileResponse
from app.tasks.chat_task import chat_task
from app.tasks.msg_embedding_task import msg_embedding_task
from app.repositories.message_repository import MessageRepository
from sqlmodel import Session
from app.database import get_session
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    msg: str = Field(..., description="empty message")

@router.post("/chats")
def post_chats(chat_request: ChatRequest):
    task = chat_task.delay(chat_request.msg, "openai", 0.7)
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


@router.get("/chats")
def get_chats(session: Session = Depends(get_session)):
        message_repository = MessageRepository(session)
        messages = message_repository.get_all_messages()
        return [{"sender": "사용자" if msg.sender_type == "user" else "서버", "text": msg.text} for msg in messages]


@router.post("/reset_chats")
def reset_chats(session: Session = Depends(get_session)):
    try:
        message_repository = MessageRepository(session)
        message_repository.delete_all_message_and_embeddings()
        
        return {"message": "모든 채팅과 임베딩 데이터가 초기화되었습니다."}
    except Exception as e:
        logger.error(f"채팅 초기화 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="채팅 초기화에 실패했습니다.")
