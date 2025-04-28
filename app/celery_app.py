import os
from dotenv import load_dotenv
from celery import Celery
from kombu.serialization import register
from app.pydanticserializer import pydantic_dumps, pydantic_loads

load_dotenv()

register('pydantic', pydantic_dumps, pydantic_loads, content_type='application/x-pydantic', content_encoding='utf-8')

app = Celery(
    "app.tasks",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
    include=[
        'app.tasks.request_bot_msg_task'
    ]
)

# 이 부분 추가
app.conf.update(
    task_serializer='pydantic',
    result_serializer='pydantic',
    event_serializer='pydantic',
    accept_content=['application/json', 'application/x-pydantic'],
    result_accept_content=['application/json', 'application/x-pydantic'],
    timezone='Asia/Seoul',
    enable_utc=True,
)

if __name__ == '__main__':
    app.start()