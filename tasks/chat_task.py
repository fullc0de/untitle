from celery_app import app
import time
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task
def chat_task(msg):
    time.sleep(1)
    logger.info(f"chat: {msg}")
    return "hello world"