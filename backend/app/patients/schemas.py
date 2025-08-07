from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr


class PatientBase(BaseModel):
    name: str
    dob: date | None = None
    medical_history: str | None = None
    email: EmailStr | None = None
    cellphone: str | None = None
    phone: str | None = None
    address: str | None = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    # All fields are optional for updates
    name: str | None = None


class Patient(PatientBase):
    id: int
    credit_balance: Decimal
    last_appointment: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
