import enum
import typing

import sqlalchemy as sa
from sqlalchemy import func, select
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.types import Boolean, Date, DateTime, Enum, Integer, Numeric, Time

from app.db.base import Base
from app.payments.models import Payment

if typing.TYPE_CHECKING:
    from app.patients.models import Patient
from app.specialties.models import Specialty

class AppointmentStatus(enum.Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    RESCHEDULED = "RESCHEDULED"


class RecurringFrequency(enum.Enum):
    WEEKLY = "WEEKLY"
    BIWEEKLY = "BIWEEKLY"


class DayOfWeek(enum.Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class Appointment(Base):
    __tablename__ = "appointments"

    id = sa.Column(Integer, primary_key=True, index=True)
    start_time = sa.Column(DateTime, nullable=False)
    end_time = sa.Column(DateTime, nullable=False)
    cost = sa.Column(Numeric(10, 2), nullable=False)
    status = sa.Column(Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.SCHEDULED)

    patient_id = sa.Column(Integer, sa.ForeignKey("patients.id"), nullable=False)
    patient = relationship("Patient", back_populates="appointments")

    specialty_id = sa.Column(Integer, sa.ForeignKey("specialties.id"), nullable=False)
    specialty = relationship("Specialty", back_populates="appointments")

    rescheduled_to_appointment_id = sa.Column(Integer, sa.ForeignKey("appointments.id"), nullable=True)

    recurring_series_id = sa.Column(Integer, sa.ForeignKey("recurring_series.id"), nullable=True)
    recurring_series = relationship("RecurringSeries", back_populates="appointments")

    payments = relationship("Payment", back_populates="appointment", order_by="desc(Payment.payment_date)")

    total_paid = column_property(
        select(func.coalesce(func.sum(Payment.amount), 0.0)).where(Payment.appointment_id == id).scalar_subquery()
    )


class RecurringSeries(Base):
    __tablename__ = "recurring_series"

    id = sa.Column(Integer, primary_key=True, index=True)
    frequency = sa.Column(Enum(RecurringFrequency), nullable=False)
    start_date = sa.Column(Date, nullable=False)
    end_date = sa.Column(Date, nullable=True)  # Either end_date or number_of_appointments will be set
    number_of_appointments = sa.Column(Integer, nullable=True)

    appointments = relationship("Appointment", back_populates="recurring_series")


class WorkingHours(Base):
    __tablename__ = "working_hours"

    id = sa.Column(Integer, primary_key=True, index=True)
    day_of_week = sa.Column(Enum(DayOfWeek), nullable=False, unique=True)
    start_time = sa.Column(Time)
    end_time = sa.Column(Time)
    is_closed = sa.Column(Boolean, default=False)
