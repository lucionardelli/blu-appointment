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
    payment_date: datetime | None = None
    appointment_id: int | None = None
    patient_id: int


class PaymentCreate(PaymentBase):
    payment_method_id: int
    pass


class PaymentUpdate(PaymentBase):
    payment_method_id: int
    pass


class Payment(PaymentBase):
    id: int
    payment_method: PaymentMethod

    model_config = ConfigDict(from_attributes=True)
