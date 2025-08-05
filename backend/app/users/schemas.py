from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str
    default_timezone: str = "UTC"

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
