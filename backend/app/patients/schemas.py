from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from decimal import Decimal

class PatientBase(BaseModel):
    name: str
    dob: Optional[date] = None
    medical_history: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    contact_address: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    # All fields are optional for updates
    name: Optional[str] = None

class Patient(PatientBase):
    id: int
    credit_balance: Decimal

    class Config:
        from_attributes = True
