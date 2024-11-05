from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 365

def create_jwt_token(user_id: int, nickname: str) -> str:
    """JWT 토큰을 생성합니다."""
    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "exp": expire,
        "user_id": user_id,
        "nickname": nickname
    }
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str) -> Optional[Dict]:
    """JWT 토큰을 검증하고 페이로드를 반환합니다."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {
            "success": True,
            "payload": payload,
            "expired": False
        }
    except jwt.ExpiredSignatureError:
        return {
            "success": False,
            "payload": None,
            "expired": True
        }
    except jwt.JWTError:
        return {
            "success": False, 
            "payload": None,
            "expired": False
        }