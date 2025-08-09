import os
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.users.crud import get_user_by_username
from app.core.security import ALGORITHM, oauth2_scheme, verify_password

if TYPE_CHECKING:
    from app.users.models import User


def authenticate_user(user: "User", password: str) -> bool:
    return user is not None and verify_password(password, user.hashed_password)


def get_current_user(db: Annotated[Session, Depends(get_db)], token: str = Depends(oauth2_scheme)) -> "User":
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception from None
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user
