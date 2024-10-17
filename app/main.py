import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
from sqlmodel import Session, select
from app.database import engine
from app.models import Item
from fastapi.staticfiles import StaticFiles
from app.apis.chats import router as chats_router

import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
admin = Admin(app, engine)

allowed_origins = os.getenv("ALLOWED_ORIGINS")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session():
    with Session(engine) as session:
        yield session

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(chats_router)


###
# 아래 부분은 프로젝트 테스트 코드임
###

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

class ItemAdmin(ModelView, model=Item):
    column_list = [Item.id, Item.name, Item.quantity]
    column_sortable_list = [Item.id, Item.name, Item.quantity]
    column_searchable_list = [Item.name]

admin.add_view(ItemAdmin)
