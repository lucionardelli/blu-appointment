from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SpecialtyPriceBase(BaseModel):
    price: Decimal = Field(..., gt=0)


class SpecialtyPriceCreate(SpecialtyPriceBase):
    pass


class SpecialtyPrice(SpecialtyPriceBase):
    id: int
    valid_from: datetime

    model_config = ConfigDict(from_attributes=True)


class MinSpecialtyInfo(BaseModel):
    """Minimal specialty info needed for calendar display"""

    id: int
    name: str
    color: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SpecialtyBase(BaseModel):
    name: str
    default_duration_minutes: int = Field(..., gt=0)
    current_price: Decimal | None
    color: str | None = None


class SpecialtyCreate(SpecialtyBase): ...


class SpecialtyUpdate(BaseModel):
    name: str | None = None
    default_duration_minutes: int | None = Field(None, gt=0)
    current_price: Decimal | None = Field(None, gt=0)
    color: str | None = None


class Specialty(SpecialtyBase):
    id: int
    prices: list[SpecialtyPrice] = []

    model_config = ConfigDict(from_attributes=True)
