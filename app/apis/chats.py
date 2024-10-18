from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse
from celery.result import AsyncResult
from app.tasks.chat_task import chat_task
import logging


logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/chat")
def chat(msg: str = Query(..., description="empty message")):
    task = chat_task.delay(msg, "openai", 0.7)
    try:
        reply = task.get(timeout=10)
        logger.info(f"Task result: {reply}")
        return {"reply": reply}
    except TimeoutError:
        return {"status": "PENDING", "message": "작업이 아직 완료되지 않았습니다. 나중에 다시 시도해주세요."}


@router.get("/chat-test")
async def chat_test():
    logger.info("chat_test")
    return FileResponse("app/static/chat.html", media_type="text/html")