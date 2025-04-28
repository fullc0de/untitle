from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session
import os
import logging

load_dotenv()

# DEBUG 환경변수 확인
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# DEBUG가 True일 때만 로깅 설정
if DEBUG:
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/annyong_db")

# DEBUG가 True일 때만 echo=True 설정
engine = create_engine(DATABASE_URL, pool_size=5, echo=DEBUG)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session