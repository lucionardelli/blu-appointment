from pydantic import BaseModel, ConfigDict


class PaymentMethodBase(BaseModel):
    name: str


class PaymentMethodCreate(PaymentMethodBase): ...


class PaymentMethodUpdate(PaymentMethodBase):
    name: str | None = None


class PaymentMethod(PaymentMethodBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
