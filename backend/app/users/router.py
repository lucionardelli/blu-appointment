from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.users.logged import get_current_user
from app.users.models import User

from . import services, schemas

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]) -> schemas.User:
    db_user = services.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    return services.create_user(db=db, user=user)


@router.get("/", response_model=schemas.User)
def read_logged_user(current_user: Annotated[User, Depends(get_current_user)]) -> schemas.User:
    return current_user


@router.put("/", response_model=schemas.User)
def update_logged_user(
    user_update: schemas.UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.User:
    updated_user = services.update_user(db=db, user_id=current_user.id, user_update=user_update)
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user


@router.put("/password", response_model=schemas.User)
def update_logged_user_password(
    password_update: schemas.UserPasswordUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.User:
    updated_user = services.update_user_password(
        db=db, user_id=current_user.id, password_update=password_update
    )
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user
