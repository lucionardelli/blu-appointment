from datetime import UTC, datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy import desc, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.types import DateTime, Integer, Numeric, String

from app.db.base import Base


class Specialty(Base):
    __tablename__ = "specialties"

    id = sa.Column(Integer, primary_key=True, index=True)
    name = sa.Column(String(255), nullable=False, unique=True)
    default_duration_minutes = sa.Column(Integer, nullable=False)

    prices = relationship("SpecialtyPrice", back_populates="specialty", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="specialty")

    @hybrid_property
    def current_price(self) -> Decimal | None:
        if not self.prices:
            return None
        return max(self.prices, key=lambda p: p.valid_from).price

    @current_price.expression
    def current_price(cls) -> Mapped[Decimal | None]:  # noqa: N805
        return (
            select(SpecialtyPrice.price)
            .where(SpecialtyPrice.specialty_id == cls.id)
            .order_by(desc(SpecialtyPrice.valid_from))
            .limit(1)
            .scalar_subquery()
        )

    @current_price.setter
    def current_price(self, value: Decimal) -> None:
        latest_price = (
            max(self.prices, key=lambda p: p.valid_from)
            if self.prices else None
        )
        if latest_price is None or latest_price.price != value:
            new_price = SpecialtyPrice(
                specialty=self,
                price=value,
                valid_from=datetime.now(UTC),
            )
            self.prices.append(new_price)


class SpecialtyPrice(Base):
    __tablename__ = "specialty_prices"

    id = sa.Column(Integer, primary_key=True, index=True)
    price = sa.Column(Numeric(10, 2), nullable=False)
    valid_from = sa.Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))

    specialty_id = sa.Column(Integer, sa.ForeignKey("specialties.id"), nullable=False)
    specialty = relationship("Specialty", back_populates="prices")
