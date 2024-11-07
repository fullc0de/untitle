from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum

class SenderType(str, Enum):
    user = "user"
    assistant = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int = Field(default=None, primary_key=True)
    text: str = Field(..., index=True)
    chatroom_id: int = Field(..., foreign_key="chatrooms.id", index=True)
    sender_type: SenderType
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
