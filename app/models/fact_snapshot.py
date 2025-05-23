from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column
from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class FactSnapshotCharacterInfo(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    relationship: Optional[str] = None
    interest_keywords: Optional[List[str]] = None
    expertise_keywords: Optional[List[str]] = None

class FactSnapshot(SQLModel, table=True):
    __tablename__ = "fact_snapshots"

    id: int = Field(default=None, primary_key=True)
    chatroom_id: int = Field(nullable=False, index=True)
    chat_id: int = Field(nullable=False)
    character_info: dict = Field(sa_column=Column(JSONB))
    conversation_summary: str = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    def set_character_info(self, character_info: FactSnapshotCharacterInfo):
        self.character_info = character_info.model_dump()

    def get_character_info(self) -> Optional[FactSnapshotCharacterInfo]:
        if self.character_info:
            return FactSnapshotCharacterInfo(**self.character_info)
        return None
