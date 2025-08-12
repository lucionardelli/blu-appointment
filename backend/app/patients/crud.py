from sqlalchemy.orm import Session, joinedload

from app.core.encryption import decrypt, encrypt

from . import models, schemas
from app.appointments.models import Appointment


def get_patient(db: Session, patient_id: int) -> models.Patient | None:
    db_patient = (
        db.query(models.Patient)
        .options(joinedload(models.Patient.referred_by))
        .filter(models.Patient.id == patient_id)
        .first()
    )
    if db_patient and db_patient.encrypted_medical_history:
        db_patient.medical_history = decrypt(db_patient.encrypted_medical_history)
    return db_patient


def get_patients(db: Session, skip: int = 0, limit: int = 100) -> list[models.Patient]:
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    for p in patients:
        if p.encrypted_medical_history:
            p.medical_history = decrypt(p.encrypted_medical_history)
    return patients


def get_patient_appointments(
    db: Session, patient_id: int, skip: int = 0, limit: int = 100
) -> list[Appointment]:
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        return []

    appointments = (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return appointments


def create_patient(db: Session, patient: schemas.PatientCreate) -> models.Patient:
    encrypted_history = encrypt(patient.medical_history) if patient.medical_history else None

    db_patient = models.Patient(
        name=patient.name,
        nickname=patient.nickname,
        dob=patient.dob,
        encrypted_medical_history=encrypted_history,
        email=patient.email,
        phone=patient.phone,
        address=patient.address,
        how_they_found_us=patient.how_they_found_us,
        referred_by_patient_id=patient.referred_by_patient_id,
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    if db_patient.referred_by_patient_id == db_patient.id:
        raise ValueError("A patient cannot be their own referrer.")

    # Decrypt for the response object
    if db_patient.encrypted_medical_history:
        db_patient.medical_history = decrypt(db_patient.encrypted_medical_history)
    return db_patient


def update_patient(db: Session, patient_id: int, patient_update: schemas.PatientUpdate) -> models.Patient | None:
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        return None

    if patient_update.referred_by_patient_id and patient_update.referred_by_patient_id == patient_id:
        raise ValueError("A patient cannot be their own referrer.")

    update_data = patient_update.model_dump(exclude_unset=True)

    if "medical_history" in update_data:
        db_patient.encrypted_medical_history = encrypt(update_data["medical_history"])
        del update_data["medical_history"]  # Don't try to set this attribute on the model

    for key, value in update_data.items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    # Decrypt for the response object
    if db_patient.encrypted_medical_history:
        db_patient.medical_history = decrypt(db_patient.encrypted_medical_history)
    return db_patient


def delete_patient(db: Session, patient_id: int) -> models.Patient | None:
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient:
        db.delete(db_patient)
        db.commit()
    return db_patient
