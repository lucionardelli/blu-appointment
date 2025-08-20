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


def get_payment(db: Session, payment_id: int) -> models.Payment | None:
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()


def get_payments(db: Session, skip: int = 0, limit: int = 100) -> list[models.Payment]:
    return db.query(models.Payment).offset(skip).limit(limit).all()


def create_payment(db: Session, payment: schemas.PaymentCreate) -> models.Payment:
    db_payment = models.Payment(**payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def update_payment(db: Session, payment_id: int, payment_update: schemas.PaymentUpdate) -> models.Payment | None:
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not db_payment:
        return None

    for key, value in payment_update.model_dump(exclude_unset=True).items():
        setattr(db_payment, key, value)

    db.commit()
    db.refresh(db_payment)
    return db_payment


def delete_payment(db: Session, payment_id: int) -> models.Payment | None:
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not db_payment:
        return None

    db.delete(db_payment)
    db.commit()
    return db_payment
