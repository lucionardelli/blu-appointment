from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class SpecialtyPriceBase(BaseModel):
    price: Decimal = Field(..., gt=0)


class SpecialtyPriceCreate(SpecialtyPriceBase):
    pass


class SpecialtyPrice(SpecialtyPriceBase):
    id: int
    valid_from: datetime

    class Config:
        from_attributes = True


class SpecialtyBase(BaseModel):
    name: str
    default_duration_minutes: int = Field(..., gt=0)


class SpecialtyCreate(SpecialtyBase):
    initial_price: Decimal = Field(..., gt=0)


class SpecialtyUpdate(BaseModel):
    name: str | None = None
    default_duration_minutes: int | None = Field(None, gt=0)


class Specialty(SpecialtyBase):
    id: int
    prices: list[SpecialtyPrice] = []

    class Config:
        from_attributes = True
