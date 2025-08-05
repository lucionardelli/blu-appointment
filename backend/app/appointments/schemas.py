from pydantic import BaseModel, Field, model_validator
from typing import List, Optional
from decimal import Decimal
from datetime import datetime, time, date
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
    cost: Optional[Decimal] = Field(None, gt=0)

class AppointmentUpdate(BaseModel):
    start_time: Optional[datetime] = None
    cost: Optional[Decimal] = Field(None, gt=0)
    status: Optional[AppointmentStatus] = None

class Appointment(AppointmentBase):
    id: int
    end_time: datetime
    cost: Decimal
    status: AppointmentStatus
    payments: List[Payment] = []

    class Config:
        from_attributes = True

# --- Recurring Series Schemas ---
class RecurringSeriesCreate(BaseModel):
    patient_id: int
    specialty_id: int
    start_time: datetime # Time of the first appointment
    frequency: RecurringFrequency

    # User must provide one of these
    end_date: Optional[date] = None
    number_of_appointments: Optional[int] = Field(None, gt=1)

    @model_validator(mode='after')
    def check_end_condition(self) -> 'RecurringSeriesCreate':
        if self.end_date is None and self.number_of_appointments is None:
            raise ValueError('Either end_date or number_of_appointments must be provided.')
        if self.end_date is not None and self.number_of_appointments is not None:
            raise ValueError('Only one of end_date or number_of_appointments should be provided.')
        return self

# --- Working Hours Schemas ---
class WorkingHoursBase(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_closed: bool = False

class WorkingHoursCreate(WorkingHoursBase):
    pass

class WorkingHoursUpdate(BaseModel):
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_closed: Optional[bool] = None

class WorkingHours(WorkingHoursBase):
    id: int

    class Config:
        from_attributes = True
