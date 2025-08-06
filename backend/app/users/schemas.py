from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    username: str
    default_timezone: str = "UTC"


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(UserBase):
    password: str | None = Field(min_length=8, default=None)


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
