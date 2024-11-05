from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.database import get_session
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class SignUpRequest(BaseModel):
    username: str
    password: str

class SignUpResponse(BaseModel):
    id: int
    username: str
    message: str = "Successfully signed up"
    token: str

@router.post("/api/signup", response_model=SignUpResponse)
async def signup(request: SignUpRequest, session: Session = Depends(get_session)):
    auth_repository = AuthRepository(session)
    auth_service = AuthService(auth_repository)
    
    result = await auth_service.signup(
        username=request.username,
        password=request.password
    )
    return SignUpResponse(id=result.id, username=result.nickname, token=result.token)


class SignInRequest(BaseModel):
    username: str
    password: str

class SignInResponse(BaseModel):
    id: int
    username: str
    token: str

@router.post("/api/signin", response_model=SignInResponse)
async def signin(request: SignInRequest, session: Session = Depends(get_session)):
    auth_repository = AuthRepository(session)
    auth_service = AuthService(auth_repository)
    
    result = await auth_service.signin(
        username=request.username,
        password=request.password
    )
    return SignInResponse(id=result.id, username=result.nickname, token=result.token)