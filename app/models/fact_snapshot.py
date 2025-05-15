from sqlalchemy import Column
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class FactSnapshot(SQLModel, table=True):
    __tablename__ = "fact_snapshots"

    id: int = Field(default=None, primary_key=True)
    chatroom_id: int = Field(nullable=False, index=True)
    chat_id: int = Field(nullable=False)
    character_info: dict = Field(sa_column=Column(JSONB))
    conversation_summary: str = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
