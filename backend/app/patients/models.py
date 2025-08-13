from datetime import UTC, date, datetime

import sqlalchemy as sa
from sqlalchemy import ForeignKey, func, select
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.types import Date, String, Text

from app.appointments.models import Appointment, Payment
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
    how_they_found_us = sa.Column(Text)

    # Self-referencing FK for referrals
    referred_by_patient_id = sa.Column(sa.Integer, ForeignKey("patients.id"), nullable=True)
    referred_by = relationship("Patient", remote_side=[id], backref="referred_patients")

    default_specialty_id = sa.Column(ForeignKey("specialties.id"))
    default_specialty = relationship("Specialty")

    appointments = relationship("Appointment", back_populates="patient")

    emergency_contacts = relationship(
        "EmergencyContact", back_populates="patient", order_by="EmergencyContact.priority"
    )

    credit_balance = column_property(
        select(func.coalesce(func.sum(Payment.amount), 0))
        .where(Payment.appointment_id.in_(select(Appointment.id).where(Appointment.patient_id == id)))
        .correlate_except(Payment)
        .scalar_subquery()
        - select(func.coalesce(func.sum(Appointment.cost), 0))
        .where(Appointment.patient_id == id)
        .correlate_except(Appointment)
        .scalar_subquery()
    )

    last_appointment = column_property(
        select(func.min(Appointment.start_time))
        .where(Appointment.patient_id == id, Appointment.start_time < datetime.now(UTC))
        .scalar_subquery()
    )
    next_appointment = column_property(
        select(func.min(Appointment.start_time))
        .where(Appointment.patient_id == id, Appointment.start_time >= datetime.now(UTC))
        .scalar_subquery()
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


class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    patient_id = sa.Column(sa.Integer, ForeignKey("patients.id"), nullable=False)
    full_name = sa.Column(String(255), nullable=False)
    patient_relationship = sa.Column(String(255))
    email = sa.Column(String(255))
    phone_number = sa.Column(String(50))
    cellphone = sa.Column(String(50))
    priority = sa.Column(sa.Integer, nullable=False, default=0)

    patient = relationship("Patient", back_populates="emergency_contacts")
