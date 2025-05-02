from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column
from sqlalchemy.orm import Mapped, relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User, Bot, Chat

class Chatroom(SQLModel, table=True):
    __tablename__ = "chatrooms"

    id: int = Field(default=None, primary_key=True)
    owner_id: int = Field(nullable=False, foreign_key="users.id")
    title: Optional[str] = Field(default=None)
    property: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}) 

    owner: Optional["User"] = Relationship(back_populates="chatrooms")
    bot: Optional["Bot"] = Relationship(back_populates="chatroom")

    # # 외래키 제약조건 없이 관계 설정
    # chats: List["Chat"] = Relationship(
    #     sa_relationship=relationship(
    #         "Chat", primaryjoin="and_(Chatroom.id==Chat.chatroom_id)", foreign_keys="Chat.chatroom_id"
    #     )
    # )
