from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db

from . import crud, schemas
from app.appointments import schemas as appt_schemas

router = APIRouter()


@router.post("/", response_model=schemas.Patient, status_code=status.HTTP_201_CREATED)
def create_patient(patient: schemas.PatientCreate, db: Annotated[Session, Depends(get_db)]) -> schemas.Patient:
    return crud.create_patient(db=db, patient=patient)


@router.get("/", response_model=list[schemas.Patient])
def read_patients(db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 100) -> list[schemas.Patient]:
    return crud.get_patients(db, skip=skip, limit=limit)


@router.get("/{patient_id}", response_model=schemas.Patient)
def read_patient(patient_id: int, db: Annotated[Session, Depends(get_db)]) -> schemas.Patient:
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return db_patient

@router.get("/{patient_id}/appointments", response_model=list[appt_schemas.Appointment])
def read_patient_appointments(
    patient_id: int, db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 100
) -> list[appt_schemas.Appointment]:
    db_appointments = crud.get_patient_appointments(db, patient_id=patient_id, skip=skip, limit=limit)
    if db_appointments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found or no appointments")
    return db_appointments

@router.put("/{patient_id}", response_model=schemas.Patient)
def update_patient(
    patient_id: int, patient: schemas.PatientUpdate, db: Annotated[Session, Depends(get_db)]
) -> schemas.Patient:
    db_patient = crud.update_patient(db, patient_id=patient_id, patient_update=patient)
    if db_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return db_patient


@router.delete("/{patient_id}", response_model=schemas.Patient)
def delete_patient(patient_id: int, db: Annotated[Session, Depends(get_db)]) -> schemas.Patient:
    db_patient = crud.delete_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return db_patient
