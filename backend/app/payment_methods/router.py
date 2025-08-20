from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.users.logged import get_current_user
from app.users.models import User

from . import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.PaymentMethod, status_code=status.HTTP_201_CREATED)
def create_payment_method(
    payment_method: schemas.PaymentMethodCreate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.PaymentMethod:
    try:
        return crud.create_payment_method(db=db, payment_method=payment_method)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None


@router.get("/", response_model=list[schemas.PaymentMethod])
def read_payment_methods(
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
) -> list[schemas.PaymentMethod]:
    payment_methods = crud.get_payment_methods(db, skip=skip, limit=limit)
    return payment_methods


@router.get("/{payment_method_id}", response_model=schemas.PaymentMethod)
def read_payment_method(
    payment_method_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.PaymentMethod:
    db_payment_method = crud.get_payment_method(db, payment_method_id=payment_method_id)
    if db_payment_method is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment method not found")
    return db_payment_method


@router.put("/{payment_method_id}", response_model=schemas.PaymentMethod)
def update_payment_method(
    payment_method_id: int,
    payment_method: schemas.PaymentMethodUpdate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.PaymentMethod:
    try:
        db_payment_method = crud.update_payment_method(db, payment_method_id=payment_method_id, payment_method_update=payment_method)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None
    if db_payment_method is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment method not found")
    return db_payment_method


@router.delete("/{payment_method_id}", response_model=schemas.PaymentMethod)
def delete_payment_method(
    payment_method_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.PaymentMethod:
    db_payment_method = crud.delete_payment_method(db, payment_method_id=payment_method_id)
    if db_payment_method is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment method not found")
    return db_payment_method
