from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.users.logged import get_current_user
from app.users.models import User

from . import services, schemas

payment_methods_router = APIRouter()
payments_router = APIRouter()


@payment_methods_router.post("/", response_model=schemas.PaymentMethod, status_code=status.HTTP_201_CREATED)
def create_payment_method(
    payment_method: schemas.PaymentMethodCreate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.PaymentMethod:
    try:
        return services.create_payment_method(db=db, payment_method=payment_method)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None


@payment_methods_router.get("/", response_model=list[schemas.PaymentMethod])
def read_payment_methods(
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
) -> list[schemas.PaymentMethod]:
    return services.get_payment_methods(db, skip=skip, limit=limit)


@payment_methods_router.get("/{payment_method_id}/", response_model=schemas.PaymentMethod)
def read_payment_method(
    payment_method_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.PaymentMethod:
    db_payment_method = services.get_payment_method(db, payment_method_id=payment_method_id)
    if db_payment_method is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment method not found")
    return db_payment_method


@payment_methods_router.put("/{payment_method_id}/", response_model=schemas.PaymentMethod)
def update_payment_method(
    payment_method_id: int,
    payment_method: schemas.PaymentMethodUpdate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.PaymentMethod:
    try:
        db_payment_method = services.update_payment_method(
            db, payment_method_id=payment_method_id, payment_method_update=payment_method
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None
    if db_payment_method is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment method not found")
    return db_payment_method


@payment_methods_router.delete("/{payment_method_id}/", response_model=schemas.PaymentMethod)
def delete_payment_method(
    payment_method_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.PaymentMethod:
    db_payment_method = services.delete_payment_method(db, payment_method_id=payment_method_id)
    if db_payment_method is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment method not found")
    return db_payment_method


@payments_router.post("/", response_model=schemas.Payment)
def create_payment(
    payment: schemas.PaymentCreate,
    db: Annotated[Session, Depends(get_db)],
) -> schemas.Payment:
    return services.create_payment(db=db, payment=payment)


@payments_router.get("/", response_model=list[schemas.Payment])
def read_payments(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[schemas.Payment]:
    return services.get_payments(db, skip=skip, limit=limit)


@payments_router.get("/{payment_id}/", response_model=schemas.Payment)
def read_payment(
    payment_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> schemas.Payment:
    db_payment = services.get_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment


@payments_router.put("/{payment_id}/", response_model=schemas.Payment)
def update_payment(
    payment_id: int,
    payment: schemas.PaymentUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> schemas.Payment:
    db_payment = services.update_payment(db, payment_id=payment_id, payment_update=payment)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment


@payments_router.delete("/{payment_id}/", response_model=schemas.Payment)
def delete_payment(
    payment_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> schemas.Payment:
    db_payment = services.delete_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment
