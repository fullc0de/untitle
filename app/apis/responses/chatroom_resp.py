from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.apis.responses.bot_resp import BotResp
from app.models.chatroom import Chatroom

class ChatroomPropertyResp(BaseModel):
    bot_name: Optional[str] = None
    latest_emotion_color: Optional[str] = None
    latest_emotion_text: Optional[str] = None
    latest_message: Optional[str] = None

class ChatroomResp(BaseModel):
    id: int
    title: Optional[str]
    property: Optional[ChatroomPropertyResp]
    owner_id: int
    created_at: datetime
    updated_at: datetime
    bot: Optional[BotResp]

    @classmethod
    def from_orm(cls, chatroom: Chatroom) -> "ChatroomResp":
        return cls(
            id=chatroom.id,
            title=chatroom.title,
            property=ChatroomPropertyResp(**chatroom.property) if chatroom.property else None,
            owner_id=chatroom.owner_id,
            created_at=chatroom.created_at,
            updated_at=chatroom.updated_at,
            bot=BotResp.from_orm(chatroom.bot) if chatroom.bot else None
        )