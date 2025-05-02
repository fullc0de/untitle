
from pydantic import BaseModel


class CreateChatParam(BaseModel):
    chatroom_id: int
    text: str
