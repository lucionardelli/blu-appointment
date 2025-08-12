from sqlalchemy.orm import Session

from app.core.security import get_password_hash

from . import models, schemas


def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        default_timezone=user.default_timezone,
        language=user.language,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> models.User | None:
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, user_id: int, password_update: schemas.UserPasswordUpdate) -> models.User | None:
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    if not user.verify_password(password_update.old_password):
        return None

    user.hashed_password = get_password_hash(password_update.new_password)
    db.commit()
    db.refresh(user)
    return user
