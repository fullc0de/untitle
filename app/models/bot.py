from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column
from app.models.user import User
from sqlmodel import Relationship

class Bot(SQLModel, table=True):
    __tablename__ = "bots"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(..., index=True)
    owner_id: int = Field(nullable=False, foreign_key="users.id")
    profile: Optional[dict] = Field(default={}, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}) 

    owner: User = Relationship(back_populates="bots")
    chatrooms: List["Chatroom"] = Relationship(back_populates="bot")