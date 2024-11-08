from fastapi import APIRouter, Depends
from app.models.user import User
from app.dependencies.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/api/user/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {"nickname": current_user.nickname}