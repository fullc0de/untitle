from typing import Any, Dict, Optional
from pydantic import BaseModel
from sqlalchemy import Column
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from enum import Enum

class SenderType(str, Enum):
    user = "user"
    bot = "bot"

class ChatContent(BaseModel):
    text: Optional[str] = None
    original_response: Optional[dict] = None
    
class ChatProperty(BaseModel):
    emotion_hex_color: Optional[str] = None
    emoticon: Optional[str] = None
    
class Chat(SQLModel, table=True):
    __tablename__ = "chats"

    id: int = Field(default=None, primary_key=True)
    content: dict = Field(sa_column=Column(JSONB))
    property: dict = Field(sa_column=Column(JSONB))
    chatroom_id: int = Field(nullable=False, index=True)
    sender_id: int = Field(nullable=False, index=True)
    sender_type: SenderType = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    def set_content(self, content: ChatContent):
        self.content = content.model_dump()

    def get_content(self) -> Optional[ChatContent]:
        if self.content:
            return ChatContent(**self.content)
        return None
    
    def set_property(self, property: ChatProperty):
        self.property = property.model_dump()

    def get_property(self) -> Optional[ChatProperty]:
        if self.property:
            return ChatProperty(**self.property)
        return None
