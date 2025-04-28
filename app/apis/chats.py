from datetime import datetime
from fastapi import APIRouter, Query, Body, Depends, HTTPException
from app.services.chat_service import ChatService
from app.services.user_service import UserService
from sqlmodel import Session
from app.database import get_session, engine
from pydantic import BaseModel, Field, field_validator
from app.dependencies.auth import get_current_user
from app.models import User, Chatroom
from app.apis import enum as api_enum
from typing import List, Dict, Any, Literal, Optional
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter()

class AttendeeParam(BaseModel):
    id: int
    name: str
    role: str

class AttendeeResp(BaseModel):
    id: int
    name: str
    is_bot: bool

class ChatroomResp(BaseModel):
    id: int
    property: Optional[dict]
    attendees: List[AttendeeResp]
    created_at: datetime
    updated_at: datetime

class CreateChatroomParam(BaseModel):
    bot_ids: List[int]
    nickname: str
    user_persona_desc: str
    age: int
    gender: str

@router.post("/api/chatrooms", response_model=ChatroomResp)
def create_chatroom(
    create_chatroom_param: CreateChatroomParam,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        chat_service = ChatService(session)
        # chatroom = chat_service.create_chatroom(
        #     current_user.id, 
        #     create_chatroom_param.nickname,
        #     create_chatroom_param.user_persona_desc,
        #     create_chatroom_param.age,
        #     create_chatroom_param.gender,
        #     create_chatroom_param.bot_ids
        # )

        # return get_chatroom_resp(chatroom, session)
        return {}                
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
        chat_service = ChatService(session)
        # chatrooms = chat_service.get_chatrooms_by_user_id(current_user.id)

        # chatroomsResp = []
        # for chatroom in chatrooms:
        #     chatroomsResp.append(get_chatroom_resp(chatroom, session))

        # logger.info(f"chatroomsResp: {json.dumps(chatroomsResp, default=str)}")
        return []

    except Exception as e:
        logger.error(f"Error in get_chatrooms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"채팅방 조회 중 오류가 발생했습니다: {str(e)}")

@router.get("/api/chatrooms/{chatroom_id}", response_model=ChatroomResp)
def get_chatroom(
    chatroom_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    chat_service = ChatService(session)
    # chatroom = chat_service.get_chatroom_by_id(chatroom_id)
    # if not chatroom:
    #     raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다.")
    return ChatroomResp(id=chatroom_id, property={}, attendees=[], created_at=datetime.now(), updated_at=datetime.now())

# class ChatParam(BaseModel):
#     chatroom_id: int
#     sender_id: int
#     msg: str

# class ChatResp(BaseModel):
#     id: int
#     text: str
#     chatroom_id: int
#     attendee_type: api_enum.SenderType = Field(serialization_alias="sender_type")
#     created_at: datetime

#     @field_validator("attendee_type", mode="before")
#     @classmethod
#     def convert_attendee_type(cls, v: AttendeeType) -> api_enum.SenderType:
#         if v == AttendeeType.user:
#             return api_enum.SenderType.user
#         else:
#             return api_enum.SenderType.bot


# @router.post("/api/chats", response_model=ChatResp)
# async def post_chats(
#     chat_param: ChatParam,
#     current_user: User = Depends(get_current_user),
#     session: Session = Depends(get_session)
# ):
#     try:
#         # 유저 메시지 저장
#         logger.info(f"user message: {chat_param.msg}")
#         logger.info(f"attendee_id: {chat_param.sender_id}")
#         logger.info(f"chatroom_id: {chat_param.chatroom_id}")
#         chat_service = ChatService(session, ChatRepository(session), UserRepository(session))
#         message = chat_service.make_turn(chat_param.msg, chat_param.chatroom_id, chat_param.sender_id, AttendeeType.user)

#         return message
#     except Exception as e:
#         logger.error(f"Error in post_chats: {str(e)}")


# @router.get("/api/chats", response_model=List[ChatResp])
# def get_chats(
#     chatroom_id: int,
#     current_user: User = Depends(get_current_user),
#     session: Session = Depends(get_session)
# ):
#     chat_service = ChatService(session, ChatRepository(session), UserRepository(session))
#     user_service = UserService(session, UserRepository(session))
#     chatroom = chat_service.get_chatroom_by_id(chatroom_id)
#     messages = chat_service.get_all_messages(chatroom_id)
#     user_persona = user_service.user_persona_by_user_id(current_user.id, chatroom_id)

#     chatsResp = []
#     for message in messages:
#         chatsResp.append(get_chat_resp(chatroom, message, user_persona, session))
#     return chatsResp


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
