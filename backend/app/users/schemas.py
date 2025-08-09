from pydantic import BaseModel, ConfigDict, Field

from app.common.enums import Language


class UserBase(BaseModel):
    username: str
    default_timezone: str = "UTC"
    language: Language = Language.ENGLISH


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    password: str | None = Field(min_length=8, default=None)
    default_timezone: str | None = None
    language: Language | None = None


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
