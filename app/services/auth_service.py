from app.repositories.auth_repository import AuthRepository
from sqlmodel import Session
from app.models import User
from app.services.transaction_service import TransactionService
from fastapi import HTTPException
from app.utils.jwt_utils import create_jwt_token
import logging

logger = logging.getLogger(__name__)

class AuthService(TransactionService):
    def __init__(self, session: Session, auth_repository: AuthRepository):
        super().__init__(session)
        self.auth_repository = auth_repository
        
    async def signup(self, username: str, password: str) -> User:
        """새로운 사용자를 등록하고 JWT 토큰을 발급합니다."""
        try:
            def transaction(session: Session):
                # 중복 사용자 확인
                existing_user = self.auth_repository.get_user_by_nickname(username)
                if existing_user:
                    raise HTTPException(status_code=409, detail="중복된 사용자입니다.")
            
                # 새 사용자 생성
                new_user = self.auth_repository.create_user(
                    nickname=username,
                    password=password,
                    role={"type": "user"}  # 기본 역할 설정
                )
                
                # JWT 토큰 생성
                token = create_jwt_token(new_user.id, new_user.nickname)
                
                # 토큰 저장
                new_user = self.auth_repository.update_user_token(new_user.id, token)

                logger.info(f"새로운 사용자가 생성되었습니다: {username}")
                return new_user
            return self.execute_in_transaction(transaction)
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"회원가입 중 오류 발생: {str(e)}")
            raise HTTPException(status_code=500, detail="회원가입 처리 중 오류가 발생했습니다.") 
    

    async def signin(self, username: str, password: str) -> User:
        """사용자 모델을 가져와서 반환합니다."""
        try:
            user = self.auth_repository.get_user_by_nickname(username)
            if not user:
                raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다.")
            
            if not user.check_password(password):
                raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")
        
            return user
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"로그인 중 오류 발생: {str(e)}")
            raise HTTPException(status_code=500, detail="로그인 처리 중 오류가 발생했습니다.")