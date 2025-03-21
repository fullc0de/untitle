import os
import json
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqladmin import Admin, ModelView
from app.database import engine
from app.models.message import Message
from fastapi.staticfiles import StaticFiles
from app.apis.chats import router as chats_router
from app.apis.auth import router as auth_router
from app.apis.users import router as users_router
from app.utils.websocket import socket_app, send_message_to_client
from app.admin.admin_setting import setup_admin
import redis.asyncio as redis
import logging


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Redis 구독자 설정
    pubsub = redis_client.pubsub()
    
    async def redis_listener():
        await pubsub.subscribe("chat_messages")
        while True:
            try:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message and message["type"] == "message":
                    logger.info(f"listener message: {message}")
                    data = json.loads(message["data"])
                    await send_message_to_client(data["message"])
            except Exception as e:
                logger.error(f"Redis 구독 오류: {str(e)}")
                await asyncio.sleep(1)
    
    # 시작 시
    task = asyncio.create_task(redis_listener())
    yield
    # 종료 시
    await pubsub.unsubscribe()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)
admin = setup_admin(app, engine)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/socket.io", socket_app)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(chats_router)
app.include_router(auth_router)
app.include_router(users_router)

###
# 아래 부분은 프로젝트 테스트 코드임
###

@app.get("/")
async def read_root():
    return FileResponse("app/static/index.html", media_type="text/html")


@app.get("/chat-test")
async def chat_test():
    logger.info("chat_test")
    return FileResponse("app/static/chat.html", media_type="text/html")

@app.get("/signup")
async def signup_page():
    return FileResponse("app/static/signup.html", media_type="text/html")

@app.get("/signin")
async def signin_page():
    return FileResponse("app/static/signin.html", media_type="text/html")

@app.get("/main")
async def main_page():
    return FileResponse("app/static/main.html", media_type="text/html")