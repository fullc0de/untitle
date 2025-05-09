from sqlmodel import Session
from app.repositories.user_repository import UserRepository
from app.services.transaction_service import TransactionService
from app.models import Bot, User
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
