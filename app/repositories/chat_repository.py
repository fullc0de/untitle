from typing import List
from sqlmodel import Session, select
from app.models import Chatroom, Bot, Chat, ChatroomPromptModifier, FactSnapshot
from app.models.chat import SenderType
import logging

logger = logging.getLogger(__name__)

class ChatRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_chatroom(self, me_id: int) -> Chatroom:
        chatroom = Chatroom(owner_id=me_id)
        chatroom.set_prompt_modifier(ChatroomPromptModifier())
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

    def get_bot_by_chatroom_id(self, chatroom_id: int) -> Bot:
        bot = self.session.exec(select(Bot).where(Bot.chatroom_id == chatroom_id)).first()
        return bot

    ## chat
    def get_all_messages(self, chatroom_id: int) -> List[Chat]:
        messages = self.session.exec(select(Chat).where(Chat.chatroom_id == chatroom_id).order_by(Chat.created_at.asc())).all()
        return messages
    
    def create_chat(self, content: dict, chatroom_id: int, sender_id: int, sender_type: SenderType) -> Chat:
        chat = Chat(content=content, chatroom_id=chatroom_id, sender_id=sender_id, sender_type=sender_type)
        self.session.add(chat)
        self.session.flush()
        return chat
    
    def get_latest_messages(self, chatroom_id: int, limit: int) -> List[Chat]:
        messages = self.session.exec(
            select(Chat)
            .where(Chat.chatroom_id == chatroom_id)
            .order_by(Chat.created_at.desc())
            .limit(limit)
        ).all()
        return messages

    ## snapshot
    def create_fact_snapshot(self, chatroom_id: int, chat_id: int, character_info: dict, summary: str) -> FactSnapshot:
        fact_snapshot = FactSnapshot(chatroom_id=chatroom_id, chat_id=chat_id, character_info=character_info, conversation_summary=summary)
        self.session.add(fact_snapshot)
        self.session.flush()
        return fact_snapshot
    
    def get_latest_fact_snapshot(self, chatroom_id: int) -> FactSnapshot:
        fact_snapshot = self.session.exec(select(FactSnapshot).where(FactSnapshot.chatroom_id == chatroom_id).order_by(FactSnapshot.created_at.desc())).first()
        return fact_snapshot
