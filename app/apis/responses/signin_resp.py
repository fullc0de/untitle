from pydantic import BaseModel


class SignInResponse(BaseModel):
    id: int
    username: str
    token: str
