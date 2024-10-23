from sqlmodel import SQLModel, Field
from typing import List
from datetime import datetime
from sqlalchemy import Column, ARRAY, Float

class MsgEmbedding(SQLModel, table=True):
    __tablename__ = "msg_embeddings"

    id: int = Field(default=None, primary_key=True)
    embedding: List[float] = Field(..., sa_column=Column(ARRAY(Float)))
    message_id: int = Field(..., foreign_key="messages.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
