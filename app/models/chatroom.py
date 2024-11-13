from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column
from typing import List

class Chatroom(SQLModel, table=True):
    __tablename__ = "chatrooms"

    id: int = Field(default=None, primary_key=True)
    property: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}) 

    # Relationships
    attendees: List["Attendee"] = Relationship()