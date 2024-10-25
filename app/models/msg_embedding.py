from sqlmodel import SQLModel, Field
from typing import List
from datetime import datetime
from sqlalchemy import Column, ARRAY, Float
from pgvector.sqlalchemy import Vector

class MsgEmbedding(SQLModel, table=True):
    __tablename__ = "msg_embeddings"

    id: int = Field(default=None, primary_key=True)
    embedding: List[float] = Field(..., sa_column=Column(Vector(3072)))
    message_id: int = Field(..., foreign_key="messages.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
