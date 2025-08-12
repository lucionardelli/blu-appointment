from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr

from app.specialties.schemas import Specialty


class PatientBase(BaseModel):
    name: str
    nickname: str | None = None
    dob: date | None = None
    medical_history: str | None = None
    email: EmailStr | None = None
    cellphone: str | None = None
    phone: str | None = None
    address: str | None = None
    default_specialty_id: int | None = None
    how_they_found_us: str | None = None
    referred_by_patient_id: int | None = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    # All fields are optional for updates
    name: str | None = None


class Patient(PatientBase):
    id: int
    credit_balance: Decimal
    last_appointment: datetime | None = None
    next_appointment: datetime | None = None
    age: int | None = None
    is_underage: bool | None = None

    model_config = ConfigDict(from_attributes=True)


class PatientFinancialSummary(BaseModel):
    total_paid: Decimal
    total_due: Decimal
    balance: Decimal


class PatientAppointmentSummary(BaseModel):
    total_appointments: int
    upcoming_appointments: int
    past_appointments: int


class PatientSummary(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class PatientDetails(Patient):
    financial_summary: PatientFinancialSummary | None = None
    appointment_summary: dict[str, PatientAppointmentSummary] | None = None
    default_specialty: Specialty | None = None
    referred_by: PatientSummary | None = None

    model_config = ConfigDict(from_attributes=True)
