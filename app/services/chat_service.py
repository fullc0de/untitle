from fastapi import HTTPException
from dotenv import load_dotenv
from app.repositories.chat_repository import ChatRepository
from app.repositories.user_repository import UserRepository
from app.models.chatroom import Chatroom
from app.models.attendee import Attendee,AttendeeType
from app.models.user import User
from typing import List
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, chat_repository: ChatRepository, user_repository: UserRepository):
        self.chat_repository = chat_repository
        self.user_repository = user_repository

    def create_chatroom(self) -> Chatroom:
        return self.chat_repository.create_chatroom()
    
    def get_chatrooms_by_user_id(self, user_id: int) -> List[Chatroom]:
        user = self.user_repository.get_attendees_by_user_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        return self.chat_repository.get_chatrooms_by_attendee_id(user_id, AttendeeType.user)
    
    def get_attendees_by_chatroom_id(self, chatroom_id: int) -> List[Attendee]:
        return self.chat_repository.get_attendees_by_chatroom_id(chatroom_id)
    
    def add_user_to_chatroom(self, chatroom_id: int, user_id: int) -> Attendee:
        return self.chat_repository.add_attendee_to_chatroom(chatroom_id, user_id, AttendeeType.user)

    def add_bot_to_chatroom(self, chatroom_id: int, bot_id: int) -> Attendee:
        return self.chat_repository.add_attendee_to_chatroom(chatroom_id, bot_id, AttendeeType.bot)
