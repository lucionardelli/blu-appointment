from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PaymentMethodBase(BaseModel):
    name: str


class PaymentMethodCreate(PaymentMethodBase): ...


class PaymentMethodUpdate(PaymentMethodBase):
    name: str | None = None


class PaymentMethod(PaymentMethodBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaymentBase(BaseModel):
    amount: Decimal
    method: PaymentMethod
    payment_date: datetime | None = None
    appointment_id: int | None = None
    patient_id: int


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
