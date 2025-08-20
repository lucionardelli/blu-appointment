from datetime import UTC, datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime, Integer, Numeric, String

from app.db.base import Base


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(String(255), nullable=False, unique=True)


class Payment(Base):
    __tablename__ = "payments"

    id = sa.Column(Integer, primary_key=True, index=True)
    amount = sa.Column(Numeric(10, 2), nullable=False)
    payment_date = sa.Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    payment_method_id = sa.Column(Integer, sa.ForeignKey("payment_methods.id"), nullable=False)
    payment_method = relationship("PaymentMethod")

    appointment_id = sa.Column(Integer, sa.ForeignKey("appointments.id"), nullable=True)
    appointment = relationship("Appointment", back_populates="payments")

    patient_id = sa.Column(Integer, sa.ForeignKey("patients.id"), nullable=False)
    patient = relationship("Patient", back_populates="payments")
