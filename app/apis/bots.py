from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.database import get_session
from app.models import User, Bot
from app.dependencies.auth import get_current_user
from app.services.chat_service import ChatService
from app.repositories.chat_repository import ChatRepository
from app.apis.responses.bot_resp import BotResp

import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/api/bots", response_model=List[BotResp])
async def get_bots(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    chat_service = ChatService(session, ChatRepository(session))
    bots = chat_service.get_bots(current_user.id)
    return bots
