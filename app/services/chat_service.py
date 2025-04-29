from fastapi import HTTPException
from dotenv import load_dotenv
from sqlmodel import Session
from app.repositories.chat_repository import ChatRepository
from app.services.transaction_service import TransactionService
from app.models import Chatroom, Chat, Bot
from typing import List, Tuple, Optional
from app.tasks.request_bot_msg_task import request_bot_msg_task
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatService(TransactionService):
    def __init__(self, session: Session, chat_repository: ChatRepository):
        super().__init__(session)
        self.chat_repository = chat_repository

    def create_chatroom(self, me_id: int) -> Chatroom:
        def transaction(session: Session):
            chatroom = self.chat_repository.create_chatroom(me_id)
            bot = self.chat_repository.create_bot(owner_id=me_id, chatroom_id=chatroom.id)
            return chatroom
        return self.execute_in_transaction(transaction)
    
    def get_chatrooms_by_user_id(self, user_id: int) -> List[Chatroom]:
        return self.chat_repository.get_chatrooms_by_user_id(user_id)
    
    def get_bots(self, owner_id: int) -> List[Bot]:
        return self.chat_repository.get_bots(owner_id)
    
    # def get_chatrooms_by_user_id(self, user_id: int) -> List[Chatroom]:
    #     user = self.user_repository.get_attendees_by_user_id(user_id)
    #     if not user:
    #         raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    #     return self.chat_repository.get_chatrooms_by_target_id(user_id, AttendeeType.user)
        
    # def get_chatroom_by_id(self, chatroom_id: int) -> Chatroom | None:
    #     chatroom = self.chat_repository.get_chatroom(chatroom_id)
    #     return chatroom
    
    # # Relationship loaders
    # def load_chatroom_attendees(self, chatroom: Chatroom) -> Chatroom:
    #     return self.chat_repository.session.refresh(chatroom, ["attendees"])
    
    # def make_turn(self, text: str, chatroom_id: int, sender_id: int, sender_type: AttendeeType) -> Message:
    #     def transaction(session: Session):
    #         msg = self.chat_repository.create_message(text, chatroom_id, sender_id, sender_type)
    #         request_bot_msg_task.delay(chatroom_id, 1.0)
    #         return msg
    #     return self.execute_in_transaction(transaction)

    # def create_message(self, text: str, chatroom_id: int, sender_id: int, sender_type: AttendeeType) -> Message:
    #     def transaction(session: Session):
    #         msg = self.chat_repository.create_message(text, chatroom_id, sender_id, sender_type)
    #         return msg
    #     return self.execute_in_transaction(transaction)
    
    # def delete_all_messages(self, chatroom_id: int):
    #     def transaction(session: Session):
    #         self.chat_repository.delete_all_messages(chatroom_id)
    #     return self.execute_in_transaction(transaction)
    
    # def get_all_messages(self, chatroom_id: int) -> List[Message]:
    #     return self.chat_repository.get_all_messages(chatroom_id)