from sqlmodel import Session
from app.repositories.chat_repository import ChatRepository
from app.repositories.user_repository import UserRepository
from app.services.transaction_service import TransactionService
from app.models import Bot, User, UserPersona
from app.services import enum
from typing import List, Tuple, Optional
from app.tasks.request_bot_msg_task import request_bot_msg_task
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserService(TransactionService):  
    def __init__(self, session: Session, user_repository: UserRepository):
        super().__init__(session)
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_user_by_id(user_id)
    
    def get_user_by_attendee_id(self, attendee_id: int) -> User:
        return self.user_repository.get_user_by_attendee_id(attendee_id)
    
    def get_bot_by_id(self, bot_id: int) -> Bot:
        return self.user_repository.get_bot_by_id(bot_id)
    
    def get_bot_by_attendee_id(self, attendee_id: int) -> Bot:
        return self.user_repository.get_bot_by_attendee_id(attendee_id)

    def user_persona_by_attendee_id(self, attendee_id: int) -> UserPersona:
        return self.user_repository.user_persona_by_attendee_id(attendee_id)

    def user_persona_by_user_id(self, user_id: int, chatroom_id: int) -> UserPersona:
        return self.user_repository.user_persona_by_user_id(user_id, chatroom_id)