from fastapi import APIRouter, Query, Body, Depends, HTTPException
from app.tasks.request_bot_msg_task import request_bot_msg_task
from app.tasks.msg_embedding_task import msg_embedding_task
from app.repositories.chat_repository import ChatRepository
from app.repositories.user_repository import UserRepository
from app.services.chat_service import ChatService
from sqlmodel import Session
from app.database import get_session, engine
from pydantic import BaseModel, Field
from app.task_models.msg_info import MsgInfo
from app.dependencies.auth import get_current_user
from app.models.user import User
from typing import List, Dict, Any, Literal
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class Attendee(BaseModel):
    id: int
    name: str
    role: str

class Chatroom(BaseModel):
    id: int
    property: Dict[str, Any]
    attendees: List[Attendee]

@router.post("/api/chatrooms")
def create_chatroom(
    attendee: Attendee,
    current_user: User = Depends(get_current_user)
):
    try:
        with Session(engine) as session:
            chat_service = ChatService(ChatRepository(session), UserRepository(session))
            
            # 트랜잭션 시작
            chatroom = chat_service.create_chatroom()
            a1 = chat_service.add_user_to_chatroom(chatroom.id, current_user.id)
            
            if attendee.role == "bot":
                a2 = chat_service.add_bot_to_chatroom(chatroom.id, attendee.id)
            else:
                a2 = chat_service.add_user_to_chatroom(chatroom.id, attendee.id)
            
            response = Chatroom(
                id=chatroom.id, 
                property=chatroom.property if chatroom.property else {}, 
                attendees=[
                    Attendee(
                        id=a1.attendee_id, 
                        name="none", 
                        role=a1.attendee_type.value
                    ), 
                    Attendee(
                        id=a2.attendee_id, 
                        name="none", 
                        role=a2.attendee_type.value
                    )
                ]
            )
            
            session.commit()
            return response
            
    except Exception as e:
        logger.error(f"채팅방 생성 중 오류 발생: {str(e)}")
        if 'session' in locals():
            session.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"채팅방 생성 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/api/chatrooms")
def get_chatrooms(
    current_user: User = Depends(get_current_user)
):
    try:
        with Session(engine) as session:
            chat_service = ChatService(ChatRepository(session), UserRepository(session))
            chatrooms = chat_service.get_chatrooms_by_user_id(current_user.id)
            
            for room in chatrooms:
                attendees = chat_service.get_attendees_by_chatroom_id(room.id)
                room.attendees = []
                for attendee in attendees:
                    role = "user" if attendee.attendee_type.value == "user" else "bot"
                    attendee_obj = Attendee(
                        id=attendee.attendee_id,
                        name="none",
                        role=role
                    )
                    room.attendees.append(attendee_obj)
            return chatrooms
    except Exception as e:
        logger.error(f"Error in get_chatrooms: {str(e)}")


class ChatRequest(BaseModel):
    msg: str = Field(..., description="empty message")

@router.post("/api/chats")
async def post_chats(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        # 유저 메시지 저장
        logger.info(f"user message: {chat_request.msg}")
        with Session(engine) as session:
            chat_repository = ChatRepository(session)
            message = chat_repository.create_message(chat_request.msg, "user")

        # 유저 메시지에 대한 임베딩 생성
        msg_embedding_task.delay([MsgInfo(msg=message.text, msg_id=message.id)])

        # 봇 메시지 생성 요청
        request_bot_msg_task.delay("openai", 0.7)

        return {"result": "success"}
    except Exception as e:
        logger.error(f"Error in post_chats: {str(e)}")


@router.get("/api/chats")
def get_chats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    chat_repository = ChatRepository(session)
    messages = chat_repository.get_all_messages()
    return [{"sender": "사용자" if msg.sender_type == "user" else "서버", "text": msg.text} for msg in messages]


@router.post("/api/reset_chats")
def reset_chats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        chat_repository = ChatRepository(session)
        chat_repository.delete_all_messages()
        
        return {"message": "모든 채팅과 임베딩 데이터가 초기화되었습니다."}
    except Exception as e:
        logger.error(f"채팅 초기화 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="채팅 초기화에 실패했습니다.")
