import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime, Integer, Numeric, String

from app.db.base import Base


class Specialty(Base):
    __tablename__ = "specialties"

    id = sa.Column(Integer, primary_key=True, index=True)
    name = sa.Column(String(255), nullable=False, unique=True)
    default_duration_minutes = sa.Column(Integer, nullable=False)

    prices = relationship("SpecialtyPrice", back_populates="specialty", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="specialty")


class SpecialtyPrice(Base):
    __tablename__ = "specialty_prices"

    id = sa.Column(Integer, primary_key=True, index=True)
    price = sa.Column(Numeric(10, 2), nullable=False)
    valid_from = sa.Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    specialty_id = sa.Column(Integer, sa.ForeignKey("specialties.id"), nullable=False)
    specialty = relationship("Specialty", back_populates="prices")
