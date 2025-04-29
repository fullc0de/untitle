from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from sqlmodel import Session
from app.database import get_session
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService
from app.apis.responses.signup_resp import SignUpResponse
from app.apis.responses.signin_resp import SignInResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/api/signup", response_model=SignUpResponse)
async def signup(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session, AuthRepository(session))
    result = await auth_service.signup(
        username=username,
        password=password
    )
    return SignUpResponse(id=result.id, username=result.nickname, token=result.token)



@router.post("/api/signin", response_model=SignInResponse)
async def signin(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    auth_service = AuthService(session, AuthRepository(session))
    result = await auth_service.signin(
        username=username,
        password=password
    )
    return SignInResponse(id=result.id, username=result.nickname, token=result.token)