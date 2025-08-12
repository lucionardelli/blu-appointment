from pydantic import BaseModel, ConfigDict, Field

from app.common.enums import Language


class UserBase(BaseModel):
    username: str
    default_timezone: str = "UTC"
    language: Language = Language.ENGLISH
    name: str | None = None
    last_name: str | None = None
    email: str | None = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    default_timezone: str | None = None
    language: Language | None = None
    name: str | None = None
    last_name: str | None = None
    email: str | None = None


class UserPasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
