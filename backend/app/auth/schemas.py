from pydantic import BaseModel

from app.users.schemas import User


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User
