from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.apis.responses.bot_resp import BotResp
from app.models.chatroom import Chatroom
import logging

logger = logging.getLogger(__name__)


class ChatroomResp(BaseModel):
    id: int
    title: Optional[str]
    property: Optional[dict]
    owner_id: int
    created_at: datetime
    updated_at: datetime
    bot: Optional[BotResp]

    @classmethod
    def from_orm(cls, chatroom: Chatroom) -> "ChatroomResp":
        logger.info(f"chatroom init")
        return cls(
            id=chatroom.id,
            title=chatroom.title,
            property=chatroom.property,
            owner_id=chatroom.owner_id,
            created_at=chatroom.created_at,
            updated_at=chatroom.updated_at,
            bot=BotResp.from_orm(chatroom.bot) if chatroom.bot else None
        )