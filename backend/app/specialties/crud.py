from decimal import Decimal

from sqlalchemy import desc
from sqlalchemy.orm import Session

from . import models, schemas


def get_specialty_by_id(db: Session, specialty_id: int) -> models.Specialty | None:
    return db.query(models.Specialty).filter(models.Specialty.id == specialty_id).first()


def get_specialty_by_name(db: Session, name: str) -> models.Specialty | None:
    return db.query(models.Specialty).filter(models.Specialty.name == name).first()


def get_specialties(db: Session, skip: int = 0, limit: int = 100) -> list[models.Specialty]:
    return db.query(models.Specialty).offset(skip).limit(limit).all()


def create_specialty(db: Session, specialty: schemas.SpecialtyCreate) -> models.Specialty:
    db_specialty = models.Specialty(
        name=specialty.name,
        default_duration_minutes=specialty.default_duration_minutes,
    )
    db.add(db_specialty)
    db.commit()
    db.refresh(db_specialty)

    # Create the initial price entry
    initial_price = models.SpecialtyPrice(
        price=specialty.initial_price,
        specialty_id=db_specialty.id,
    )
    db.add(initial_price)
    db.commit()
    db.refresh(db_specialty)  # Refresh again to load the new price relationship

    return db_specialty


def update_specialty(
    db: Session, specialty_id: int, specialty_update: schemas.SpecialtyUpdate
) -> models.Specialty | None:
    db_specialty = get_specialty_by_id(db, specialty_id)
    if not db_specialty:
        return None

    update_data = specialty_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_specialty, key, value)

    db.commit()
    db.refresh(db_specialty)
    return db_specialty


def add_specialty_price(
    db: Session, specialty_id: int, price_create: schemas.SpecialtyPriceCreate
) -> models.Specialty | None:
    db_specialty = get_specialty_by_id(db, specialty_id)
    if not db_specialty:
        return None

    new_price = models.SpecialtyPrice(
        price=price_create.price,
        specialty_id=specialty_id,
    )
    db.add(new_price)
    db.commit()
    db.refresh(db_specialty)
    return db_specialty


def get_current_price_for_specialty(db: Session, specialty_id: int) -> Decimal | None:
    price_entry = (
        db.query(models.SpecialtyPrice)
        .filter(models.SpecialtyPrice.specialty_id == specialty_id)
        .order_by(desc(models.SpecialtyPrice.valid_from))
        .first()
    )

    return price_entry.price if price_entry else None
