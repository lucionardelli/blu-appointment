from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db

from . import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.Patient, status_code=status.HTTP_201_CREATED)
def create_patient(patient: schemas.PatientCreate, db: Annotated[Session, Depends(get_db)]) -> schemas.Patient:
    """Create a new patient."""
    return crud.create_patient(db=db, patient=patient)


@router.get("/", response_model=list[schemas.Patient])
def read_patients(db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 100) -> list[schemas.Patient]:
    """Retrieve all patients."""
    return crud.get_patients(db, skip=skip, limit=limit)


@router.get("/{patient_id}", response_model=schemas.Patient)
def read_patient(patient_id: int, db: Annotated[Session, Depends(get_db)]) -> schemas.Patient:
    """Retrieve a single patient by ID."""
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return db_patient


@router.put("/{patient_id}", response_model=schemas.Patient)
def update_patient(
    patient_id: int, patient: schemas.PatientUpdate, db: Annotated[Session, Depends(get_db)]
) -> schemas.Patient:
    """Update a patient's details."""
    db_patient = crud.update_patient(db, patient_id=patient_id, patient_update=patient)
    if db_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return db_patient


@router.delete("/{patient_id}", response_model=schemas.Patient)
def delete_patient(patient_id: int, db: Annotated[Session, Depends(get_db)]) -> schemas.Patient:
    """Delete a patient."""
    db_patient = crud.delete_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return db_patient
