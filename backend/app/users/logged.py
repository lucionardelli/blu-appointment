from __future__ import annotations

import os
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.core.security import ALGORITHM, oauth2_scheme, verify_password
from app.db.base import get_db
from app.users.services import get_user_by_username

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from app.users.models import User


def authenticate_user(user: User, password: str) -> bool:
    return user is not None and verify_password(password, user.hashed_password)


def validate_token(db: Session, token: str) -> User | None:
    """Validate a token and return the user, or None if invalid."""
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    return get_user_by_username(db, username)


def get_current_user(db: Annotated[Session, Depends(get_db)], token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = validate_token(db, token)
    if user is None:
        raise credentials_exception
    return user
