from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr


class PatientBase(BaseModel):
    name: str
    dob: date | None = None
    medical_history: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    contact_address: str | None = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    # All fields are optional for updates
    name: str | None = None


class Patient(PatientBase):
    id: int
    credit_balance: Decimal

    model_config = ConfigDict(from_attributes=True)
