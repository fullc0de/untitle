from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class AttendeeType(str, Enum):
    user = "user"
    bot = "bot"

class Attendee(SQLModel, table=True):
    __tablename__ = "attendees"

    id: int = Field(default=None, primary_key=True)
    chatroom_id: int = Field(..., foreign_key="chatrooms.id", index=True)
    target_id: int = Field(..., index=True)
    attendee_type: AttendeeType