from datetime import timedelta
from typing import Annotated

from app.auth.schemas import Token
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
)
from app.db.base import get_db
from app.users.crud import get_user_by_username
from app.users.logged import authenticate_user
from app.users.schemas import User
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    db: Annotated[Session, Depends(get_db)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = get_user_by_username(db, form_data.username)
    if not user or not authenticate_user(user, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer", user=user)
