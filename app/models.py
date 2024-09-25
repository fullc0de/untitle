from sqlmodel import SQLModel, Field

class Item(SQLModel, table=True):
    __tablename__ = 'items'
    id: int | None = Field(default=None, primary_key=True)
    name: str
    quantity: int | None = Field(default=None)