from fastapi import HTTPException
from dotenv import load_dotenv
from sqlmodel import Session
from app.repositories.chat_repository import ChatRepository
from app.repositories.user_repository import UserRepository
from app.services.transaction_service import TransactionService
from app.models.chatroom import Chatroom
from app.models.attendee import Attendee,AttendeeType
from app.models.user import User
from app.models.message import Message
from app.services import enum
from typing import List, Tuple, Optional
from app.tasks.request_bot_msg_task import request_bot_msg_task
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
            a1 = self.chat_repository.add_attendee_to_chatroom(chatroom.id, me_id, AttendeeType.user)
            match peer_type:
                case enum.AttendeeType.bot:
                    a2 = self.chat_repository.add_attendee_to_chatroom(chatroom.id, peer_id, AttendeeType.bot)
                case enum.AttendeeType.user:
                    a2 = self.chat_repository.add_attendee_to_chatroom(chatroom.id, peer_id, AttendeeType.user)
            return chatroom, a1, a2
        
        return self.transaction_service.execute_in_transaction(transaction)
    
    def get_chatrooms_by_user_id(self, user_id: int) -> List[Chatroom]:
        user = self.user_repository.get_attendees_by_user_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        return self.chat_repository.get_chatrooms_by_target_id(user_id, AttendeeType.user)
        
    # Relationship loaders
    def load_chatroom_attendees(self, chatroom: Chatroom) -> Chatroom:
        return self.chat_repository.session.refresh(chatroom, ["attendees"])
    
    def make_turn(self, text: str, chatroom_id: int, sender_id: int, sender_type: AttendeeType) -> Message:
        def transaction(session: Session):
            msg = self.chat_repository.create_message(text, chatroom_id, sender_id, sender_type)
            attendees = self.chat_repository.get_attendees_by_chatroom_id(chatroom_id, AttendeeType.bot)
            bot_attendee_id = attendees[0].id
            request_bot_msg_task.delay(chatroom_id, bot_attendee_id, 0.7)
            return msg
        return self.transaction_service.execute_in_transaction(transaction)

    def create_message(self, text: str, chatroom_id: int, sender_id: int, sender_type: AttendeeType) -> Message:
        def transaction(session: Session):
            msg = self.chat_repository.create_message(text, chatroom_id, sender_id, sender_type)
            return msg
        return self.transaction_service.execute_in_transaction(transaction)
    
    def delete_all_messages(self, chatroom_id: int):
        def transaction(session: Session):
            self.chat_repository.delete_all_messages(chatroom_id)
        return self.transaction_service.execute_in_transaction(transaction)