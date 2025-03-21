from sqlmodel import SQLModel, Field
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column
from typing import Optional
import hashlib

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    nickname: str = Field(..., index=True)
    password: Optional[str] = Field(default=None)
    role: dict = Field(sa_column=Column(JSONB))
    token: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}) 

    def set_password(self, password: str):
        self.password = hashlib.md5(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        return self.password == hashlib.md5(password.encode()).hexdigest()