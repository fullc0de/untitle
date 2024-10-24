
from pydantic import BaseModel

class MsgInfo(BaseModel):
    msg: str
    msg_id: int
