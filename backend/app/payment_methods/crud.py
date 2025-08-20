from sqlalchemy.orm import Session

from . import models, schemas


def get_payment_method(db: Session, payment_method_id: int) -> models.PaymentMethod | None:
    return db.query(models.PaymentMethod).filter(models.PaymentMethod.id == payment_method_id).first()


def get_payment_methods(db: Session, skip: int = 0, limit: int = 100) -> list[models.PaymentMethod]:
    return db.query(models.PaymentMethod).offset(skip).limit(limit).all()


def create_payment_method(db: Session, payment_method: schemas.PaymentMethodCreate) -> models.PaymentMethod:
    db_payment_method = models.PaymentMethod(name=payment_method.name)
    db.add(db_payment_method)
    db.commit()
    db.refresh(db_payment_method)
    return db_payment_method


def update_payment_method(
    db: Session, payment_method_id: int, payment_method_update: schemas.PaymentMethodUpdate
) -> models.PaymentMethod | None:
    db_payment_method = db.query(models.PaymentMethod).filter(models.PaymentMethod.id == payment_method_id).first()
    if not db_payment_method:
        return None
    update_data = payment_method_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_payment_method, key, value)
    db.commit()
    db.refresh(db_payment_method)
    return db_payment_method


def delete_payment_method(db: Session, payment_method_id: int) -> models.PaymentMethod | None:
    db_payment_method = db.query(models.PaymentMethod).filter(models.PaymentMethod.id == payment_method_id).first()
    if db_payment_method:
        db.delete(db_payment_method)
        db.commit()
    return db_payment_method
