from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Query, HTTPException
from sqladmin import Admin, ModelView
from sqlmodel import Session, select
from .database import engine
from .models import Item
from celery.result import AsyncResult
from tasks.task1 import add
from tasks.chat_task import chat_task

import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
admin = Admin(app, engine)

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/db-test")
def test_db(session: Session = Depends(get_session)):
    try:
        result = session.exec(select(Item)).first()
        return {"message": "Database connection successful", "result": "Data retrieved" if result else "No data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.post("/items/", response_model=Item)
def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/add")
def add_numbers(
    a: int = Query(..., description="첫 번째 숫자"),
    b: int = Query(..., description="두 번째 숫자")
):
    try:
        # 입력값 검증
        a = int(a)
        b = int(b)
    except ValueError:
        raise HTTPException(status_code=400, detail="a와 b는 유효한 정수여야 합니다.")

    # Celery task 비동기 호출
    logger.info(f"Calling add task with arguments: a={a}, b={b}")
    task = add.delay(a, b)
    logger.info(f"Task ID: {task.id}")

    try:
        result = task.get(timeout=2)
        logger.info(f"Task result: {result}")
        return {"result": result}
    except TimeoutError:
        return {"status": "PENDING", "message": "작업이 아직 완료되지 않았습니다. 나중에 다시 시도해주세요."}


@app.get("/chat")
def chat(msg: str = Query(..., description="empty message")):
    task = chat_task.delay(msg)
    try:
        reply = task.get(timeout=2)
        logger.info(f"Task result: {reply}")
        return {"reply": reply}
    except TimeoutError:
        return {"status": "PENDING", "message": "작업이 아직 완료되지 않았습니다. 나중에 다시 시도해주세요."}


class ItemAdmin(ModelView, model=Item):
    column_list = [Item.id, Item.name, Item.quantity]
    column_sortable_list = [Item.id, Item.name, Item.quantity]
    column_searchable_list = [Item.name]

admin.add_view(ItemAdmin)