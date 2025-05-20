from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column
from sqlalchemy.orm import Mapped, relationship
from typing import List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.models import User, Bot, Chat

class ChatroomPromptModifier(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    relationship: Optional[str] = None

class ChatroomProperty(BaseModel):
    latest_emotion_color: Optional[str] = None
    latest_emotion_text: Optional[str] = None

class Chatroom(SQLModel, table=True):
    __tablename__ = "chatrooms"

    id: int = Field(default=None, primary_key=True)
    owner_id: int = Field(nullable=False, foreign_key="users.id")
    title: Optional[str] = Field(default=None)
    prompt_modifier: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSONB))
    property: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSONB))
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

    def set_prompt_modifier(self, modifier: ChatroomPromptModifier):
        self.prompt_modifier = modifier.model_dump()

    def set_property(self, property: ChatroomProperty):
        self.property = property.model_dump()

    def get_prompt_modifier(self) -> Optional[ChatroomPromptModifier]:
        if self.prompt_modifier:
            return ChatroomPromptModifier(**self.prompt_modifier)
        return None

    def get_property(self) -> Optional[ChatroomProperty]:
        if self.property:
            return ChatroomProperty(**self.property)
        return None

