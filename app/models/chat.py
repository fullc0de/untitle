from sqlalchemy import Column
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from enum import Enum

class SenderType(str, Enum):
    user = "user"
    bot = "bot"

class Chat(SQLModel, table=True):
    __tablename__ = "chats"

    id: int = Field(default=None, primary_key=True)
    content: dict = Field(sa_column=Column(JSONB))
    chatroom_id: int = Field(nullable=False, index=True)
    sender_id: int = Field(nullable=False, index=True)
    sender_type: SenderType = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
