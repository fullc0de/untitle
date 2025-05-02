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

    @classmethod
    def from_orm(cls, bot: Bot) -> "BotResp":
        return cls(
            id=bot.id,
            name=bot.name,
            owner_id=bot.owner_id,
            chatroom_id=bot.chatroom_id,
            profile=bot.profile,
            created_at=bot.created_at,
            updated_at=bot.updated_at
        )
