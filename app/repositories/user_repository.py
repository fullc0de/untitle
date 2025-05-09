from typing import List
from sqlmodel import Session, select
from app.models import User
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.exec(select(User).where(User.id == user_id)).first()