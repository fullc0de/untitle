
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.apis.responses.bot_resp import BotResp
from app.models.chatroom import Chatroom



class ChatroomResp(BaseModel):
    id: int
    title: Optional[str]
    property: Optional[dict]
    owner_id: int
    created_at: datetime
    updated_at: datetime
    bot: Optional[BotResp]

    def __init__(self, chatroom: Chatroom):
        self.id = chatroom.id
        self.title = chatroom.title
        self.property = chatroom.property
        self.owner_id = chatroom.owner_id
        self.created_at = chatroom.created_at
        self.updated_at = chatroom.updated_at
        self.bot = BotResp(chatroom.bot) if chatroom.bot else None