from app.repositories.auth_repository import AuthRepository
from app.models import User
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository
        
    async def signup(self, username: str, password: str) -> User:
        """새로운 사용자를 등록합니다."""
        try:
            # 중복 사용자 확인
            existing_user = self.auth_repository.get_user_by_nickname(username)
            if existing_user:
                raise HTTPException(status_code=409, detail="중복된 사용자입니다.")
            
            # 새 사용자 생성
            new_user = self.auth_repository.create_user(
                nickname=username,
                role={"type": "user"}  # 기본 역할 설정
            )
            
            logger.info(f"새로운 사용자가 생성되었습니다: {username}")
            return new_user
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"회원가입 중 오류 발생: {str(e)}")
            raise HTTPException(status_code=500, detail="회원가입 처리 중 오류가 발생했습니다.") 