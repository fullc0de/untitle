from fastapi import HTTPException
from dotenv import load_dotenv
from sqlmodel import Session
from app.repositories.chat_repository import ChatRepository
from app.repositories.user_repository import UserRepository
from app.services.transaction_service import TransactionService
from app.models.chatroom import Chatroom
from app.models.attendee import Attendee,AttendeeType
from app.models.message import Message
from app.services import enum
from typing import List, Tuple, Optional
from app.tasks.request_bot_msg_task import request_bot_msg_task
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatService(TransactionService):
    def __init__(self, session: Session, chat_repository: ChatRepository, user_repository: UserRepository):
        super().__init__(session)
        self.chat_repository = chat_repository
        self.user_repository = user_repository

    def create_chatroom(self, me_id: int, nickname: str, user_persona_desc: str, age: int, gender: str, peer_ids: List[int]) -> Tuple[Chatroom]:
        def transaction(session: Session):
            chatroom = self.chat_repository.create_chatroom()
            me_attendee = self.chat_repository.add_attendee_to_chatroom(chatroom.id, me_id, AttendeeType.user)
            self.chat_repository.create_user_persona(me_id, chatroom.id, me_attendee.id, nickname, user_persona_desc, age, gender)
            for peer_id in peer_ids:
                self.chat_repository.add_attendee_to_chatroom(chatroom.id, peer_id, AttendeeType.bot)
            return chatroom
        return self.execute_in_transaction(transaction)
    
    def get_chatrooms_by_user_id(self, user_id: int) -> List[Chatroom]:
        user = self.user_repository.get_attendees_by_user_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        return self.chat_repository.get_chatrooms_by_target_id(user_id, AttendeeType.user)
        
    def get_chatroom_by_id(self, chatroom_id: int) -> Chatroom | None:
        chatroom = self.chat_repository.get_chatroom(chatroom_id)
        return chatroom
    
    # Relationship loaders
    def load_chatroom_attendees(self, chatroom: Chatroom) -> Chatroom:
        return self.chat_repository.session.refresh(chatroom, ["attendees"])
    
    def make_turn(self, text: str, chatroom_id: int, sender_id: int, sender_type: AttendeeType) -> Message:
        def transaction(session: Session):
            msg = self.chat_repository.create_message(text, chatroom_id, sender_id, sender_type)
            request_bot_msg_task.delay(chatroom_id, 1.0)
            return msg
        return self.execute_in_transaction(transaction)

    def create_message(self, text: str, chatroom_id: int, sender_id: int, sender_type: AttendeeType) -> Message:
        def transaction(session: Session):
            msg = self.chat_repository.create_message(text, chatroom_id, sender_id, sender_type)
            return msg
        return self.execute_in_transaction(transaction)
    
    def delete_all_messages(self, chatroom_id: int):
        def transaction(session: Session):
            self.chat_repository.delete_all_messages(chatroom_id)
        return self.execute_in_transaction(transaction)
    
    def get_all_messages(self, chatroom_id: int) -> List[Message]:
        return self.chat_repository.get_all_messages(chatroom_id)