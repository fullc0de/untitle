from typing import List
from sqlmodel import Session, select
from app.models import User
import logging

from app.models import Chatroom, Bot

logger = logging.getLogger(__name__)

class ChatRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_chatroom(self, me_id: int) -> Chatroom:
        chatroom = Chatroom(owner_id=me_id)
        self.session.add(chatroom)
        self.session.flush()
        return chatroom
    
    def get_chatroom_by_id(self, chatroom_id: int) -> Chatroom:
        chatroom = self.session.get(Chatroom, chatroom_id)
        return chatroom
    
    def get_chatrooms_by_user_id(self, user_id: int) -> List[Chatroom]:
        chatrooms = self.session.exec(select(Chatroom).where(Chatroom.owner_id == user_id)).all()
        return chatrooms
    
    
    ## bot
    def create_bot(self, owner_id: int, chatroom_id: int) -> Bot:
        bot = Bot(owner_id=owner_id, chatroom_id=chatroom_id)
        self.session.add(bot)
        self.session.flush()
        return bot
    
    def get_bots(self, owner_id: int) -> List[Bot]:
        bots = self.session.exec(select(Bot).where(Bot.owner_id == owner_id)).all()
        return bots
