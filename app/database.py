from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/fastapi_db")

engine = create_engine(DATABASE_URL, pool_size=5)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session