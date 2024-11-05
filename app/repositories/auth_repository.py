from sqlmodel import Session, select
from app.models import User
import logging

logger = logging.getLogger(__name__)

class AuthRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def create_user(self, nickname: str, role: dict) -> User:
        """새로운 사용자를 생성합니다."""
        try:
            new_user = User(nickname=nickname, role=role)
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            return new_user
        except Exception as e:
            logger.error(f"사용자 생성 중 오류 발생: {str(e)}")
            raise
            
    def get_user_by_nickname(self, nickname: str) -> User | None:
        """닉네임으로 사용자를 조회합니다."""
        try:
            statement = select(User).where(User.nickname == nickname)
            return self.session.exec(statement).first()
        except Exception as e:
            logger.error(f"사용자 조회 중 오류 발생: {str(e)}")
            raise 