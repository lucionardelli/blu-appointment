from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.appointments import schemas as appt_schemas
from app.db import get_db
from app.users.logged import get_current_user
from app.users.models import User

from . import services, schemas

router = APIRouter()


@router.post("/", response_model=schemas.Patient, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient: schemas.PatientCreate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.Patient:
    try:
        return services.create_patient(db=db, patient=patient)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None


@router.get("/", response_model=schemas.PaginatedPatientsResponse)
def read_patients(
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
    query: str = "",
    skip: int = 0,
    limit: int = 100,
) -> schemas.PaginatedPatientsResponse:
    total_count, patients = services.get_patients(db, query=query, skip=skip, limit=limit)
    return schemas.PaginatedPatientsResponse(total_count=total_count, items=patients)


@router.get("/{patient_id}/", response_model=schemas.PatientDetails)
def read_patient(
    patient_id: int, db: Annotated[Session, Depends(get_db)], _current_user: Annotated[User, Depends(get_current_user)]
) -> schemas.PatientDetails:
    db_patient = services.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    db_patient.financial_summary = services.get_financial_summary(db, patient_id=patient_id)
    db_patient.appointment_summary = services.get_appointment_summary(db, patient_id=patient_id)

    return schemas.PatientDetails.model_validate(db_patient)


@router.get("/{patient_id}/appointments/", response_model=list[appt_schemas.Appointment])
def read_patient_appointments(
    patient_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
) -> list[appt_schemas.Appointment]:
    db_appointments = services.get_patient_appointments(db, patient_id=patient_id, skip=skip, limit=limit)
    if db_appointments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found or no appointments")
    return db_appointments


@router.put("/{patient_id}/", response_model=schemas.Patient)
def update_patient(
    patient_id: int,
    patient: schemas.PatientUpdate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.Patient:
    try:
        db_patient = services.update_patient(db, patient_id=patient_id, patient_update=patient)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None
    if db_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return db_patient


@router.get("/{patient_id}/payments/", response_model=list[appt_schemas.Payment])
def read_patient_payments(
    patient_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[appt_schemas.Payment]:
    db_payments = services.get_patient_payments(db, patient_id=patient_id)
    if db_payments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found or no payments")
    return db_payments


@router.delete("/{patient_id}/", response_model=schemas.Patient)
def delete_patient(
    patient_id: int, db: Annotated[Session, Depends(get_db)], _current_user: Annotated[User, Depends(get_current_user)]
) -> schemas.Patient:
    db_patient = services.delete_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return db_patient


@router.post(
    "/{patient_id}/emergency_contacts/",
    response_model=schemas.EmergencyContact,
    status_code=status.HTTP_201_CREATED,
)
def create_emergency_contact(
    patient_id: int,
    contact: schemas.EmergencyContactCreate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.EmergencyContact:
    db_patient = services.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return services.create_emergency_contact(db=db, patient_id=patient_id, contact=contact)


@router.get("/{patient_id}/emergency_contacts/", response_model=list[schemas.EmergencyContact])
def read_emergency_contacts(
    patient_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[schemas.EmergencyContact]:
    db_patient = services.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return services.get_emergency_contacts_for_patient(db=db, patient_id=patient_id)


@router.get(
    "/{patient_id}/emergency_contacts/{contact_id}/",
    response_model=schemas.EmergencyContact,
)
def read_emergency_contact(
    patient_id: int,
    contact_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.EmergencyContact:
    db_contact = services.get_emergency_contact(db, contact_id=contact_id)
    if db_contact is None or db_contact.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emergency contact not found")
    return db_contact


@router.put(
    "/{patient_id}/emergency_contacts/{contact_id}/",
    response_model=schemas.EmergencyContact,
)
def update_emergency_contact(
    patient_id: int,
    contact_id: int,
    contact: schemas.EmergencyContactUpdate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.EmergencyContact:
    db_contact = services.get_emergency_contact(db, contact_id=contact_id)
    if db_contact is None or db_contact.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emergency contact not found")
    return services.update_emergency_contact(db=db, contact_id=contact_id, contact_update=contact)


@router.delete(
    "/{patient_id}/emergency_contacts/{contact_id}/",
    response_model=schemas.EmergencyContact,
)
def delete_emergency_contact(
    patient_id: int,
    contact_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.EmergencyContact:
    db_contact = services.get_emergency_contact(db, contact_id=contact_id)
    if db_contact is None or db_contact.patient_id != patient_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emergency contact not found")
    return services.delete_emergency_contact(db=db, contact_id=contact_id)
