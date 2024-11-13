from datetime import datetime
from fastapi import APIRouter, Query, Body, Depends, HTTPException
from app.tasks.request_bot_msg_task import request_bot_msg_task
from app.tasks.msg_embedding_task import msg_embedding_task
from app.repositories.chat_repository import ChatRepository
from app.repositories.user_repository import UserRepository
from app.services.transaction_service import TransactionService
from app.services.chat_service import ChatService
from sqlmodel import Session
from app.database import get_session, engine
from pydantic import BaseModel, Field, field_validator, field_serializer
from app.task_models.msg_info import MsgInfo
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.attendee import Attendee, AttendeeType
from app.models.message import SenderType
from app.apis import enum as api_enum
from typing import List, Dict, Any, Literal, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class AttendeeParam(BaseModel):
    id: int
    name: str
    role: str

class ChatroomResp(BaseModel):
    id: int
    property: Optional[dict]
    attendees: List[Attendee]

@router.post("/api/chatrooms", response_model=ChatroomResp)
def create_chatroom(
    attendee: AttendeeParam,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        chat_service = ChatService(TransactionService(session))
        chatroom, a1, a2 = chat_service.create_chatroom(current_user.id, attendee.id, attendee.role)
        return chatroom
            
    except Exception as e:
        logger.error(f"채팅방 생성 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"채팅방 생성 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/api/chatrooms", response_model=List[ChatroomResp])
def get_chatrooms(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        chat_service = ChatService(TransactionService(session))
        chatrooms = chat_service.get_chatrooms_by_user_id(current_user.id)
        return chatrooms
    except Exception as e:
        logger.error(f"Error in get_chatrooms: {str(e)}")


class ChatParam(BaseModel):
    msg: str

class ChatResp(BaseModel):
    id: int
    text: str
    chatroom_id: int
    sender_type: api_enum.SenderType
    created_at: datetime

    @field_validator("sender_type", mode="before")
    @classmethod
    def convert_sender_type(cls, v: SenderType) -> api_enum.SenderType:
        if v == SenderType.user:
            return api_enum.SenderType.user
        else:
            return api_enum.SenderType.bot


@router.post("/api/chats", response_model=ChatResp)
async def post_chats(
    chat_param: ChatParam,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        # 유저 메시지 저장
        logger.info(f"user message: {chat_param.msg}")
        chat_repository = ChatRepository(session)
        message = chat_repository.create_message(chat_param.msg, "user")

        # 유저 메시지에 대한 임베딩 생성
        msg_embedding_task.delay([MsgInfo(msg=message.text, msg_id=message.id)])

        # 봇 메시지 생성 요청
        request_bot_msg_task.delay("openai", 0.7)

        return message
    except Exception as e:
        logger.error(f"Error in post_chats: {str(e)}")


@router.get("/api/chats", response_model=List[ChatResp])
def get_chats(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    chat_repository = ChatRepository(session)
    messages = chat_repository.get_all_messages()
    return messages


@router.post("/api/reset_chats")
def reset_chats(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        chat_repository = ChatRepository(session)
        chat_repository.delete_all_messages()
        
        return {"message": "모든 채팅과 임베딩 데이터가 초기화되었습니다."}
    except Exception as e:
        logger.error(f"채팅 초기화 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="채팅 초기화에 실패했습니다.")
