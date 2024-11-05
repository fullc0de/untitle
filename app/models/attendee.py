from sqlmodel import SQLModel, Field
from enum import Enum

class AttendeeType(str, Enum):
    user = "user"
    bot = "bot"

class Attendee(SQLModel, table=True):
    __tablename__ = "attendees"

    id: int = Field(default=None, primary_key=True)
    session_id: int = Field(..., foreign_key="sessions.id", index=True)
    attendee_id: int = Field(..., index=True)
    attendee_type: AttendeeType 