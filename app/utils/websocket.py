import os
import socketio
import logging
from typing import Optional
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