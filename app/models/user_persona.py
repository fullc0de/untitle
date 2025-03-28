from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional

class Gender(str, Enum):
    male = "male"
    female = "female"
    non_binary = "non-binary"

class UserPersona(SQLModel, table=True):
    __tablename__ = "user_personas"

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(..., foreign_key="users.id", index=True)
    attendee_id: int = Field(..., foreign_key="attendees.id", index=True)
    chatroom_id: int = Field(..., foreign_key="chatrooms.id", index=True)
    nickname: str = Field(...)
    age: Optional[int] = Field(default=None)
    gender: Optional[Gender] = Field(default=None)
    description: Optional[str] = Field(default=None) 