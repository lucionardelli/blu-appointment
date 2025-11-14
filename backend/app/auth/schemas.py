from pydantic import BaseModel

from app.users.schemas import User


class Token(BaseModel):
    user: User
