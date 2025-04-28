from sqlmodel import Session
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
    def __init__(self, session: Session):
        super().__init__(session)

