import sqlalchemy as sa
from sqlalchemy import func, select
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.types import Date, Numeric, String, Text

from app.appointments.models import Appointment
from app.db.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(String(255), nullable=False)
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

    appointments = relationship("Appointment", back_populates="patient")

    last_appointment = column_property(
        select(func.max(Appointment.start_time)).where(Appointment.patient_id == id).scalar_subquery()
    )
