# ruff: noqa: PLC0414
import csv
import os
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.appointments.models import (
    Appointment as Appointment,
)
from app.appointments.models import DayOfWeek
from app.appointments.models import (
    Payment as Payment,
)
from app.appointments.models import (
    RecurringSeries as RecurringSeries,
)
from app.appointments.models import (
    WorkingHours as WorkingHours,
)
from app.core.security import get_password_hash
from app.db.base import engine
from app.patients.models import Patient as Patient
from app.specialties.models import Specialty
from app.specialties.models import SpecialtyPrice as SpecialtyPrice
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
            exists = session.execute(select(User).where(User.username == row["username"].lower())).first()
            if not exists:
                # Get password from env's variable PASS_<username>
                raw_pass = os.getenv(f"PASS_{row.get('username', '').upper()}")
                if not raw_pass:
                    raise ValueError(f"Password for user {row['username']} not found in environment variables.")
                user = User(
                    username=row["username"].lower(),
                    hashed_password=get_password_hash(raw_pass),
                    default_timezone=row["default_timezone"],
                    language=row["language"],
                )
                session.add(user)
        session.commit()


def seed_working_hours(file_path: Path) -> None:
    with Session(engine) as session, file_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                day_of_week = DayOfWeek[row["day_of_week"]]
            except KeyError:
                raise ValueError(f"Invalid day_of_week value: {row['day_of_week']}") from None

            working_hours = session.execute(select(WorkingHours).where(WorkingHours.day_of_week == day_of_week)).first()
            if not working_hours:
                working_hours = WorkingHours(day_of_week=day_of_week)
                session.add(working_hours)

            working_hours.start_time = (
                datetime.strptime(row["start_time"], "%H:%M").time() if row["start_time"] else None  # noqa: DTZ007
            )
            working_hours.end_time = datetime.strptime(row["end_time"], "%H:%M").time() if row["end_time"] else None  # noqa: DTZ007
            working_hours.is_closed = bool(int(row["is_closed"]))
        session.commit()
