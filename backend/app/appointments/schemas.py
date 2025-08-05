from datetime import date, datetime, time
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator

from .models import AppointmentStatus, PaymentMethod, RecurringFrequency


# --- Payment Schemas ---
class PaymentBase(BaseModel):
    amount: Decimal = Field(..., gt=0)
    method: PaymentMethod


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int
    payment_date: datetime

    class Config:
        from_attributes = True


# --- Appointment Schemas ---
class AppointmentBase(BaseModel):
    start_time: datetime
    patient_id: int
    specialty_id: int


class AppointmentCreate(BaseModel):
    patient_id: int
    specialty_id: int
    start_time: datetime
    # Cost is optional; if not provided, it will be fetched from the specialty's current price
    cost: Decimal | None = Field(None, gt=0)


class AppointmentUpdate(BaseModel):
    start_time: datetime | None = None
    cost: Decimal | None = Field(None, gt=0)
    status: AppointmentStatus | None = None


class Appointment(AppointmentBase):
    id: int
    end_time: datetime
    cost: Decimal
    status: AppointmentStatus
    payments: list[Payment] = []

    class Config:
        from_attributes = True


# --- Recurring Series Schemas ---
class RecurringSeriesCreate(BaseModel):
    patient_id: int
    specialty_id: int
    start_time: datetime  # Time of the first appointment
    frequency: RecurringFrequency

    # User must provide one of these
    end_date: date | None = None
    number_of_appointments: int | None = Field(None, gt=1)

    @model_validator(mode="after")
    def check_end_condition(self) -> "RecurringSeriesCreate":
        if self.end_date is None and self.number_of_appointments is None:
            msg = "Either end_date or number_of_appointments must be provided."
            raise ValueError(msg)
        if self.end_date is not None and self.number_of_appointments is not None:
            msg = "Only one of end_date or number_of_appointments should be provided."
            raise ValueError(msg)
        return self


# --- Working Hours Schemas ---
class WorkingHoursBase(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: time | None = None
    end_time: time | None = None
    is_closed: bool = False


class WorkingHoursCreate(WorkingHoursBase):
    pass


class WorkingHoursUpdate(BaseModel):
    start_time: time | None = None
    end_time: time | None = None
    is_closed: bool | None = None


class WorkingHours(WorkingHoursBase):
    id: int

    class Config:
        from_attributes = True
