from pydantic import BaseModel


class SignUpResponse(BaseModel):
    id: int
    username: str
    message: str = "Successfully signed up"
    token: str
