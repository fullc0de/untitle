import socketio
import logging
import json
import asyncio
from fastapi import FastAPI
import redis.asyncio as redis
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=allowed_origins)
socket_app = socketio.ASGIApp(sio)
connected_id: Optional[str] = None

@sio.event
async def connect(sid, environ):
    global connected_id
    connected_id = sid
    logger.info(f"클라이언트 연결됨: {sid}")

@sio.event
async def disconnect(sid):
    global connected_id
    connected_id = None
    logger.info(f"클라이언트 연결 해제됨: {sid}")

async def send_message_to_client(message: str):
    global connected_id
    if connected_id:
        await sio.emit('message', {'data': message}, room=connected_id)
        logger.info(f"메시지 전송됨: {message}")
    else:
        logger.warning("연결된 클라이언트가 없습니다.") 


redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

async def init_redis_subscriber(app: FastAPI):
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

    @app.on_event("startup")
    async def start_redis_listener():
        asyncio.create_task(redis_listener())
    
    @app.on_event("shutdown")
    async def shutdown_redis():
        await pubsub.unsubscribe()