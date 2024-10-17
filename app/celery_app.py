import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

app = Celery(
    "app.tasks",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
    include=['app.tasks.chat_task']
)

# 이 부분 추가
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Seoul',
    enable_utc=True,
)

if __name__ == '__main__':
    app.start()