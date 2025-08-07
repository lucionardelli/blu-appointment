from datetime import date, datetime, UTC

import sqlalchemy as sa
from sqlalchemy import ForeignKey, func, select
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.types import Date, Numeric, String, Text

from app.appointments.models import Appointment
from app.db.base import Base

UNDERAGE_LIMIT = 18  # Define the age limit for underage patients


class Patient(Base):
    __tablename__ = "patients"
    __table_args__ = (sa.UniqueConstraint("name", name="uq_patient_name"),)

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(String(255), nullable=False, unique=True)
    nickname = sa.Column(String(255), index=True)
    dob = sa.Column(Date)

    # This will store the encrypted medical history as a string.
    # The actual encryption/decryption will be handled at the application level.
    encrypted_medical_history = sa.Column(Text)

    email = sa.Column(String(255), unique=True, index=True)
    cellphone = sa.Column(String(50), unique=True, index=True)
    phone = sa.Column(String(50))
    address = sa.Column(Text)

    # To track credit/debt. Positive for credit, negative for debt.
    credit_balance = sa.Column(Numeric(10, 2), nullable=False, server_default="0.00")

    default_specialty_id = sa.Column(ForeignKey("specialties.id"))
    default_specialty = relationship("Specialty")

    appointments = relationship("Appointment", back_populates="patient")

    last_appointment = column_property(
        select(func.min(Appointment.start_time)).where(Appointment.patient_id == id, Appointment.start_time < datetime.now(UTC)).scalar_subquery()
    )
    next_appointment = column_property(
        select(func.min(Appointment.start_time)).where(Appointment.patient_id == id, Appointment.start_time >= datetime.now(UTC)).scalar_subquery()
    )

    @property
    def age(self) -> int | None:
        if self.dob:
            today = date.today()  # noqa: DTZ011
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

        return None

    @property
    def is_underage(self) -> bool | None:
        return self.age and self.age < UNDERAGE_LIMIT
