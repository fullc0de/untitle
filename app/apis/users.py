from fastapi import APIRouter, Depends
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.apis.responses.user_resp import UserResp
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/api/user/me", response_model=UserResp)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResp.from_orm(current_user)
