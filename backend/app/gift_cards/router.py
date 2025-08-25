from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.gift_cards import models, schemas, services
from app.users.logged import get_current_user
from app.users.models import User

router = APIRouter()


@router.post("/", response_model=schemas.GiftCard, status_code=status.HTTP_201_CREATED)
def create_gift_card(
    gift_card: schemas.GiftCardCreate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> models.GiftCard:
    try:
        service = services.GiftCardService(db)
        return service.create_gift_card(gift_card=gift_card)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None


@router.get("/", response_model=list[schemas.GiftCard])
def read_gift_cards(
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[models.GiftCard]:
    service = services.GiftCardService(db)
    return service.list_gift_cards()


@router.get("/{gift_card_id}/", response_model=schemas.GiftCard)
def read_gift_card(
    gift_card_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> models.GiftCard:
    service = services.GiftCardService(db)
    db_gift_card = service.get_gift_card(gift_card_id=gift_card_id)
    if db_gift_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gift card not found")
    return db_gift_card


@router.get("/code/{code}/", response_model=schemas.GiftCard)
def read_gift_card_by_code(
    code: str,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> models.GiftCard:
    service = services.GiftCardService(db)
    db_gift_card = service.get_gift_card_by_code(code=code)
    if db_gift_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gift card not found")
    return db_gift_card


@router.put("/{gift_card_id}/", response_model=schemas.GiftCard)
def update_gift_card(
    gift_card_id: int,
    gift_card: schemas.GiftCardUpdate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> models.GiftCard:
    service = services.GiftCardService(db)
    db_gift_card = service.update_gift_card(gift_card_id=gift_card_id, gift_card=gift_card)
    if db_gift_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gift card not found")
    return db_gift_card


@router.delete("/{gift_card_id}/", response_model=schemas.GiftCard)
def deactivate_gift_card(
    gift_card_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> models.GiftCard:
    service = services.GiftCardService(db)
    db_gift_card = service.deactivate_gift_card(gift_card_id=gift_card_id)
    if db_gift_card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gift card not found")
    return db_gift_card
