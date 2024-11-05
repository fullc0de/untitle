from fastapi import Depends, HTTPException, Header
from typing import Optional
from app.utils.jwt_utils import verify_jwt_token
from app.repositories.auth_repository import AuthRepository
from app.models.user import User
from sqlmodel import Session
from app.database import get_session
import logging

logger = logging.getLogger(__name__)

async def get_current_user(
    authorization: Optional[str] = Header(None),
    session: Session = Depends(get_session)
) -> User:
    """현재 인증된 사용자를 반환하는 의존성 함수입니다."""
    if not authorization:
        raise HTTPException(
            status_code=401, 
            detail="인증 토큰이 필요합니다."
        )
        
    try:
        token = authorization.replace("Bearer ", "")
        result = verify_jwt_token(token)
        
        if not result["success"]:
            if result["expired"]:
                raise HTTPException(
                    status_code=401,
                    detail="만료된 토큰입니다."
                )
            raise HTTPException(
                status_code=401,
                detail="유효하지 않은 토큰입니다." 
            )
            
        auth_repository = AuthRepository(session)
        user = auth_repository.get_user_by_id(result["payload"]["user_id"])
        
        if not user or user.token != token:
            raise HTTPException(
                status_code=401,
                detail="존재하지 않은 사용자의 토큰입니다."
            )
            
        return user
        
    except Exception as e:
        logger.error(f"인증 처리 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=401, 
            detail="인증 처리 중 오류가 발생했습니다."
        ) 