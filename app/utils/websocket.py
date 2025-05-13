import os
import socketio
import logging
import sys
from typing import Optional
from dotenv import load_dotenv
import json

load_dotenv()

# 로깅 설정을 더 명시적으로 구성
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# StreamHandler를 명시적으로 추가
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

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

async def send_message_to_client(message):
    global connected_id
    if connected_id:
        try:
            # bytes 데이터를 UTF-8 문자열로 디코딩
            if isinstance(message['data'], bytes):
                message_str = message['data'].decode('utf-8')
            else:
                message_str = message['data']
            await sio.emit('message', message_str, room=connected_id)
            logger.info(f"메시지 전송됨: {message_str}")
        except Exception as e:
            logger.error(f"메시지 전송 중 오류 발생: {str(e)}")
    else:
        logger.warning("연결된 클라이언트가 없습니다.") 