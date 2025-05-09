from datetime import datetime
from pydantic import BaseModel
from app.models import User

class UserResp(BaseModel):
    id: int
    nickname: str
    profile: dict
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, user: User) -> "UserResp":
        return cls(
            id=user.id,
            nickname=user.nickname,
            profile=user.profile,
            created_at=user.created_at,
            updated_at=user.updated_at
        )