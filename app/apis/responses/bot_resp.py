from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.bot import Bot

class BotResp(BaseModel):
    id: int
    name: Optional[str]
    owner_id: int
    chatroom_id: int
    profile: Optional[dict]
    created_at: datetime
    updated_at: datetime

    def __init__(self, bot: Bot):
        self.id = bot.id
        self.name = bot.name
        self.owner_id = bot.owner_id
        self.chatroom_id = bot.chatroom_id
        self.profile = bot.profile
        self.created_at = bot.created_at
        self.updated_at = bot.updated_at
