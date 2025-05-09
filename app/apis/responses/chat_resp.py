from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.apis.responses.bot_resp import BotResp
from app.models import Chatroom, Chat
from app.apis.enum import SenderType

class ChatResp(BaseModel):
    id: int
    content: dict
    chatroom_id: int
    sender_id: int
    sender_type: SenderType
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, chat: Chat) -> "ChatResp":
        return cls(
            id=chat.id,
            content=chat.content,
            chatroom_id=chat.chatroom_id,
            sender_id=chat.sender_id,
            sender_type=chat.sender_type,
            created_at=chat.created_at,
            updated_at=chat.updated_at
        )