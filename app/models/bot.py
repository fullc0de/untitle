from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column
from sqlmodel import Relationship

if TYPE_CHECKING:
    from app.models import User, Chatroom

class Bot(SQLModel, table=True):
    __tablename__ = "bots"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(..., nullable=True, index=True)
    owner_id: int = Field(nullable=False, foreign_key="users.id")
    chatroom_id: int = Field(nullable=False, foreign_key="chatrooms.id")
    profile: Optional[dict] = Field(default={}, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}) 

    owner: Optional["User"] = Relationship(back_populates="bots")
    chatroom: Optional["Chatroom"] = Relationship(back_populates="bot")