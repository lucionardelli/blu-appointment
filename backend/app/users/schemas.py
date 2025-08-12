from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, SecretStr, StringConstraints

from app.common.enums import Language

UsernameString = Annotated[
    str, StringConstraints(min_length=4, strip_whitespace=True, to_lower=True, pattern=r"^[a-zA-Z0-9_]+$")
]


class UserBase(BaseModel):
    username: UsernameString = Field(
        description="Must be at least 4 characters long and can only contain letters, numbers, and underscores."
    )
    default_timezone: str = "UTC"
    language: Language = Language.ENGLISH
    name: str | None = None
    last_name: str | None = None
    email: str | None = None


class UserCreate(UserBase):
    password: SecretStr = Field(min_length=8)


class UserUpdate(BaseModel):
    default_timezone: str | None = None
    language: Language | None = None
    name: str | None = None
    last_name: str | None = None
    email: str | None = None


class UserPasswordUpdate(BaseModel):
    old_password: SecretStr = Field(min_length=8)
    new_password: SecretStr = Field(min_length=8)


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
