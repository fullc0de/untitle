from sqlmodel import SQLModel, Field

class AttendeesRelationship(SQLModel, table=True):
    __tablename__ = "attendees_relationship"

    id: int = Field(default=None, primary_key=True)
    chatroom_id: int = Field(..., foreign_key="chatrooms.id", index=True)
    relationship: str = Field(...) 