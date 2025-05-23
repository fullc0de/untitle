from datetime import datetime
from fastapi import APIRouter, Query, Body, Depends, HTTPException
from app.apis.enum import SenderType
from app.repositories.chat_repository import ChatRepository
from app.services.chat_service import ChatService
from app.services.user_service import UserService
from sqlmodel import Session
from app.database import get_session, engine
from pydantic import BaseModel, Field, field_validator
from app.dependencies.auth import get_current_user
from app.models import User, Chatroom
from app.apis.request_params.chat_param import CreateChatParam
from app.apis.responses.chatroom_resp import ChatroomResp
from app.apis.responses.chat_resp import ChatResp
from typing import List
import logging
import json



logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/chatrooms", response_model=ChatroomResp)
def create_chatroom(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        chat_service = ChatService(session, ChatRepository(session))
        chatroom = chat_service.create_chatroom(current_user.id)
        return ChatroomResp.from_orm(chatroom)               
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
        chat_service = ChatService(session, ChatRepository(session))
        chatrooms = chat_service.get_chatrooms_by_user_id(current_user.id)
        chatrooms.sort(key=lambda x: x.updated_at, reverse=True)
        return [ChatroomResp.from_orm(chatroom) for chatroom in chatrooms]
    except Exception as e:
        logger.error(f"Error in get_chatrooms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"채팅방 조회 중 오류가 발생했습니다: {str(e)}")

@router.get("/api/chatrooms/{chatroom_id}", response_model=ChatroomResp)
def get_chatroom(
    chatroom_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        chat_service = ChatService(session, ChatRepository(session))
        chatroom = chat_service.get_chatroom_by_id(chatroom_id)
        resp = ChatroomResp.from_orm(chatroom)
        logger.info(f"chatroomResp: {json.dumps(resp, default=str)}")
        return resp
    except Exception as e:
        logger.error(f"Error in get_chatroom: {str(e)}")
        raise HTTPException(status_code=500, detail=f"채팅방 조회 중 오류가 발생했습니다: {str(e)}")


@router.post("/api/chats", response_model=ChatResp)
async def post_chats(
    chat_param: CreateChatParam,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        # 유저 메시지 저장
        logger.info(f"user message: {chat_param.text}")
        logger.info(f"chatroom_id: {chat_param.chatroom_id}")
        chat_service = ChatService(session, ChatRepository(session))
        chat = chat_service.make_turn(chat_param.text, chat_param.chatroom_id, current_user.id)
        return ChatResp.from_orm(chat)
    except Exception as e:
        logger.error(f"Error in post_chats: {str(e)}")


@router.get("/api/chats", response_model=List[ChatResp])
def get_chats(
    chatroom_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    chat_service = ChatService(session, ChatRepository(session))
    messages = chat_service.get_all_messages(chatroom_id)
    return [ChatResp.from_orm(message) for message in messages]

# @router.post("/api/reset_chats")
# def reset_chats(
#     chatroom_id: int,
#     current_user: User = Depends(get_current_user),
#     session: Session = Depends(get_session)
# ):
#     try:
#         chat_service = ChatService(session, ChatRepository(session), UserRepository(session))
#         chat_service.delete_all_messages(chatroom_id)        
#         return {"message": "모든 채팅과 임베딩 데이터가 초기화되었습니다."}
#     except Exception as e:
#         logger.error(f"채팅 초기화 중 오류 발생: {str(e)}")
#         raise HTTPException(status_code=500, detail="채팅 초기화에 실패했습니다.")



########################################################
## helper functions
########################################################
# def get_chatroom_resp(chatroom: Chatroom, session: Session) -> ChatroomResp:
#     user_service = UserService(session, UserRepository(session))

#     attendeesResp = []
#     for a in chatroom.attendees:
#         if a.attendee_type == AttendeeType.bot:
#             bot = user_service.get_bot_by_attendee_id(a.id)
#             attendeesResp.append(AttendeeResp(id=a.id, name=bot.name, is_bot=True))
#         else:
#             user_persona = user_service.user_persona_by_attendee_id(a.id)
#             attendeesResp.append(AttendeeResp(id=a.id, name=user_persona.nickname, is_bot=False))

#     return ChatroomResp(
#         id=chatroom.id,
#         property=chatroom.property,
#         attendees=attendeesResp,
#         created_at=chatroom.created_at,
#         updated_at=chatroom.updated_at
#     )


# def get_chat_resp(chatroom: Chatroom, message: Message, user_persona: UserPersona, session: Session) -> ChatResp:
#     resp = ChatResp(
#         id=message.id,
#         text=message.text,
#         chatroom_id=chatroom.id,
#         attendee_type=message.attendee_type,
#         created_at=message.created_at
#     )

#     def create_formatted_msg(name: str, message: str, attendee_id: int, is_user: bool = False) -> dict:
#         return {
#             "name": name,
#             "message": message,
#             "attendee_id": attendee_id,
#             "is_user": is_user,
#             "is_narrator": name == "narrator"
#         }

#     if message.attendee_type == AttendeeType.bot:
#         pass
#         # msg_json = json.loads(message.text)
#         # formatted_messages = [
#         #     create_formatted_msg(
#         #         msg.get("name", "Unknown"),
#         #         msg.get("message", ""),
#         #         msg.get("attendee_id", None),
#         #         msg.get("name", "Unknown") == user_persona.nickname
#         #     )
#         #     for msg in msg_json.get("messages", [])
#         # ]
#     else:
#         formatted_messages = [create_formatted_msg(user_persona.nickname, message.text, user_persona.attendee_id)]
#         resp.text = json.dumps({"messages": formatted_messages})
    
#     logger.info(f"raw message: {message.text}")
#     logger.info(f"formatted_messages: {resp.text}")
    
#     return resp
