from datetime import UTC, date, datetime, time
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator, computed_field, field_validator, field_serializer

from app.payments.schemas import Payment
from app.specialties.schemas import MinSpecialtyInfo

from .models import (
    AppointmentStatus,
    DayOfWeek,
    RecurringFrequency,
)

class AppointmentBase(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime

    @field_validator('start_time', 'end_time', mode='before')
    def ensure_utc(cls, v):
        if isinstance(v, datetime) and v.tzinfo is None:
            # Assume naive datetimes are UTC
            return v.replace(tzinfo=UTC)
        return v

    @field_serializer('start_time', 'end_time')
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.isoformat().replace('+00:00', 'Z')

    specialty: MinSpecialtyInfo


class AppointmentCreate(BaseModel):
    patient_id: int
    specialty_id: int
    start_time: datetime
    # End time is optional; if not provided, it will be set to start_time + specialty's default duration
    end_time: datetime | None = None
    # Cost is optional; if not provided, it will be fetched from the specialty's current price
    cost: Decimal | None = Field(None, ge=0)

    @field_validator('start_time', 'end_time', mode='before')
    def ensure_utc(cls, v):
        if isinstance(v, datetime) and v.tzinfo is None:
            # Assume naive datetimes are UTC
            return v.replace(tzinfo=UTC)
        return v

    @field_serializer('start_time', 'end_time')
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.isoformat().replace('+00:00', 'Z')


class AppointmentUpdate(BaseModel):
    start_time: datetime
    end_time: datetime
    cost: Decimal | None = Field(None, ge=0)
    status: AppointmentStatus | None = None
    specialty_id: int | None = None
    patient_id: int | None = None

    @field_validator('start_time', 'end_time', mode='before')
    def ensure_utc(cls, v):
        if isinstance(v, datetime) and v.tzinfo is None:
            # Assume naive datetimes are UTC
            return v.replace(tzinfo=UTC)
        return v

    @field_serializer('start_time', 'end_time')
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.isoformat().replace('+00:00', 'Z')



class MinPatientInfo(BaseModel):
    """Minimal patient info needed for calendar display"""

    id: int
    name: str


class Appointment(AppointmentBase):
    cost: Decimal
    status: AppointmentStatus
    payments: list[Payment] = []
    total_paid: Decimal = Field(0, ge=0)
    suggested_treatment_duration_minutes: int | None = None

    patient: MinPatientInfo

    @computed_field
    @property
    def cancelled(self) -> bool:
        return self.status == AppointmentStatus.CANCELLED

    model_config = ConfigDict(from_attributes=True)


class AppointmentMetrics(BaseModel):
    total_appointments: int
    total_revenue: Decimal
    total_charged: Decimal
    total_due: Decimal
    period_start: date
    period_end: date

    model_config = ConfigDict(from_attributes=True)


class DashboardMetrics(BaseModel):
    appointments_today: int
    appointments_this_week: int
    expected_revenue_last_month: Decimal
    expected_revenue_this_month: Decimal
    total_charged_last_month: Decimal
    total_charged_this_month: Decimal
    total_due_last_month: Decimal
    total_due_this_month: Decimal

    model_config = ConfigDict(from_attributes=True)


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


class WorkingHoursBase(BaseModel):
    day_of_week: DayOfWeek = Field(alias="dayOfWeek")
    start_time: time | None = Field(None, alias="startTime")
    end_time: time | None = Field(None, alias="endTime")
    is_closed: bool = False


class WorkingHoursCreate(WorkingHoursBase):
    pass


class WorkingHoursUpdate(BaseModel):
    start_time: time | None = None
    end_time: time | None = None
    is_closed: bool | None = None


class WorkingHours(WorkingHoursBase):
    id: int

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
