from fastapi import APIRouter, Query, Body, Depends, HTTPException
from fastapi.responses import FileResponse
from app.tasks.request_bot_msg_task import request_bot_msg_task
from app.tasks.msg_embedding_task import msg_embedding_task
from app.repositories.message_repository import MessageRepository
from sqlmodel import Session
from app.database import get_session, engine
from pydantic import BaseModel, Field
from app.utils.websocket import send_message_to_client
from app.task_models.msg_info import MsgInfo
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    msg: str = Field(..., description="empty message")

@router.post("/chats")
async def post_chats(chat_request: ChatRequest):
    try:
        # 유저 메시지 저장
        logger.info(f"user message: {chat_request.msg}")
        with Session(engine) as session:
            message_repository = MessageRepository(session)
            message = message_repository.create_message(chat_request.msg, "user")

        # 유저 메시지에 대한 임베딩 생성
        msg_embedding_task.delay([MsgInfo(msg=message.text, msg_id=message.id)])

        # 봇 메시지 생성 요청
        request_bot_msg_task.delay("openai", 0.7)

        return {"result": "success"}
    except Exception as e:
        logger.error(f"Error in post_chats: {str(e)}")


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
