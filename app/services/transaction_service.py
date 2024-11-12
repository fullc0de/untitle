from sqlalchemy.orm import Session
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransactionService:
    def __init__(self, session: Session):
        self.session = session
        
    def execute_in_transaction(self, callback):
        try:
            result = callback(self.session)
            self.session.commit()
            return result
        except Exception as e:
            self.session.rollback()
            logger.error(f"트랜잭션 중 오류 발생: {str(e)}")
            raise e
