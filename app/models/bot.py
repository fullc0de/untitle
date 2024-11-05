from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column

class Bot(SQLModel, table=True):
    __tablename__ = "bots"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(..., index=True)
    ai_model: str = Field(..., index=True)
    property: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}) 