from fastapi import HTTPException
from dotenv import load_dotenv
from sqlmodel import Session
from app.repositories.chat_repository import ChatRepository
from app.repositories.user_repository import UserRepository
from app.services.transaction_service import TransactionService
from app.models.chatroom import Chatroom
from app.models.attendee import Attendee,AttendeeType
from app.models.user import User
from app.services import enum
from typing import List, Tuple
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self, transaction_service: TransactionService):
        self.transaction_service = transaction_service
        self.chat_repository = ChatRepository(self.transaction_service.session)
        self.user_repository = UserRepository(self.transaction_service.session)

    def create_chatroom(self, me_id: int, peer_id: int, peer_type: enum.AttendeeType) -> Tuple[Chatroom, Attendee, Attendee]:
        def transaction(session: Session):
            chatroom = self.chat_repository.create_chatroom()
            a1 = self.add_user_to_chatroom(chatroom.id, me_id) 
            match peer_type:
                case AttendeeType.bot:
                    a2 = self.add_bot_to_chatroom(chatroom.id, peer_id)
                case AttendeeType.user:
                    a2 = self.add_user_to_chatroom(chatroom.id, peer_id)
            return chatroom, a1, a2
        
        return self.transaction_service.execute_in_transaction(transaction)
    
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


    # Relationship loaders
    def load_chatroom_attendees(self, chatroom: Chatroom) -> Chatroom:
        return self.chat_repository.session.refresh(chatroom, ["attendees"])