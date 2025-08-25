from datetime import date
from pydantic import BaseModel, ConfigDict
from app.patients.schemas import Patient
from app.specialties.schemas import Specialty

class GiftCardBase(BaseModel):
    specialty_id: int
    number_of_sessions: int
    expiration_date: date
    to_patient_id: int | None = None


class GiftCardCreate(GiftCardBase):
    from_patient_ids: list[int]


class GiftCardUpdate(GiftCardBase):
    specialty_id: int | None = None
    number_of_sessions: int | None = None
    expiration_date: date | None = None


class GiftCard(GiftCardBase):
    id: int
    code: str
    sessions_left: int
    is_active: bool
    from_patients: list[Patient] = []
    to_patient: Patient | None = None
    specialty: Specialty

    model_config = ConfigDict(from_attributes=True)
