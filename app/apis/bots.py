from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.database import get_session
from app.models import User, Bot
from app.dependencies.auth import get_current_user
import logging

from app.services.user_service import UserService

logger = logging.getLogger(__name__)
router = APIRouter()

class BotResp(BaseModel):
    id: int
    name: str
    profile: dict
    created_at: datetime
    updated_at: datetime

@router.get("/api/bots")
async def get_bots(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user_service = UserService(session)
    # bots = user_service.get_bots()
    # return [convert_bot_to_bot_resp(bot) for bot in bots]
    return []


def convert_bot_to_bot_resp(bot: Bot) -> BotResp:
    return BotResp(
        id=bot.id,
        name=bot.name,
        profile=bot.profile,
        created_at=bot.created_at,
        updated_at=bot.updated_at
    )