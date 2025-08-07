import csv
from decimal import Decimal
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.base import engine
from app.specialties.models import Specialty
from app.users.models import User


def seed_specialties(file_path: Path) -> None:
    with Session(engine) as session, file_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            exists = session.execute(select(Specialty).where(Specialty.name == row["name"])).first()
            if not exists:
                specialty = Specialty(
                    name=row["name"],
                    default_duration_minutes=int(row["default_duration_minutes"]),
                    current_price=Decimal(row["current_price"]),
                )
                session.add(specialty)
        session.commit()


def seed_users(file_path: Path) -> None:
    with Session(engine) as session, file_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            exists = session.execute(select(User).where(User.username == row["username"])).first()
            if not exists:
                user = User(
                    username=row["username"],
                    hashed_password=get_password_hash(row["password"]),
                    default_timezone=row["default_timezone"],
                )
                session.add(user)
        session.commit()
