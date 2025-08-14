from datetime import UTC, datetime

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.appointments.models import Appointment, Payment
from app.core.encryption import decrypt, encrypt

from . import models, schemas


def get_financial_summary(db: Session, patient_id: int) -> schemas.PatientFinancialSummary:
    total_paid = (
        db.query(func.sum(Payment.amount)).join(Appointment).filter(Appointment.patient_id == patient_id).scalar()
    ) or 0

    total_due = (db.query(func.sum(Appointment.cost)).filter(Appointment.patient_id == patient_id).scalar()) or 0

    return schemas.PatientFinancialSummary(
        total_paid=total_paid,
        total_due=total_due,
        balance=total_paid - total_due,
    )


def get_appointment_summary(db: Session, patient_id: int) -> schemas.AppointmentSummary:
    appointments = db.query(Appointment).filter(Appointment.patient_id == patient_id).all()

    # Do this on db side if performance becomes an issue
    total_appointments = len(appointments)
    upcoming_appointments = sum(1 for app in appointments if app.start_time.replace(tzinfo=UTC) > datetime.now(tz=UTC))
    past_appointments = total_appointments - upcoming_appointments

    specialty_counts = {}
    for app in appointments:
        if not app.specialty_id:
            continue  # Skip appointments without a specialty

        this_specialty_count = specialty_counts.setdefault(app.specialty_id, {"total": 0, "upcoming": 0, "past": 0})
        this_specialty_count["total"] += 1
        if app.start_time.replace(tzinfo=UTC) > datetime.now(tz=UTC):
            this_specialty_count["upcoming"] += 1
        else:
            this_specialty_count["past"] += 1

    return schemas.AppointmentSummary(
        total_appointments=total_appointments,
        upcoming_appointments=upcoming_appointments,
        past_appointments=past_appointments,
        specialty_counts=specialty_counts,
    )


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


def get_patients(db: Session, skip: int = 0, limit: int = 100) -> tuple[int, list[models.Patient]]:
    total_patients = db.query(models.Patient).count()
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    for p in patients:
        if p.encrypted_medical_history:
            p.medical_history = decrypt(p.encrypted_medical_history)
    return total_patients, patients


def get_patient_appointments(db: Session, patient_id: int, skip: int = 0, limit: int = 100) -> list[Appointment]:
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        return []

    return db.query(Appointment).filter(Appointment.patient_id == patient_id).offset(skip).limit(limit).all()


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


def create_emergency_contact(
    db: Session, patient_id: int, contact: schemas.EmergencyContactCreate
) -> models.EmergencyContact:
    db_contact = models.EmergencyContact(**contact.model_dump(), patient_id=patient_id)

    existing_contacts_count = (
        db.query(models.EmergencyContact).filter(models.EmergencyContact.patient_id == patient_id).count()
    )
    db_contact.priority = existing_contacts_count + 1
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_emergency_contact(db: Session, contact_id: int) -> models.EmergencyContact | None:
    return db.query(models.EmergencyContact).filter(models.EmergencyContact.id == contact_id).first()


def get_emergency_contacts_for_patient(db: Session, patient_id: int) -> list[models.EmergencyContact]:
    return (
        db.query(models.EmergencyContact)
        .filter(models.EmergencyContact.patient_id == patient_id)
        .order_by(models.EmergencyContact.priority)
        .all()
    )


def update_emergency_contact(
    db: Session,
    contact_id: int,
    contact_update: schemas.EmergencyContactUpdate,
) -> models.EmergencyContact | None:
    db_contact = db.query(models.EmergencyContact).filter(models.EmergencyContact.id == contact_id).first()
    if not db_contact:
        return None

    # If the priority is being updated, ensure it is unique
    if contact_update.priority is not None and contact_update.priority > len(db_contact.patient.emergency_contacts):
        raise ValueError("Priority must be less than or equal to the number of emergency contacts.")

    update_data = contact_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_contact, key, value)

    for another_contact in db_contact.patient.emergency_contacts:
        if another_contact.id != contact_id and another_contact.priority >= db_contact.priority:
            another_contact.priority += 1

    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_emergency_contact(db: Session, contact_id: int) -> models.EmergencyContact | None:
    db_contact = db.query(models.EmergencyContact).filter(models.EmergencyContact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def search_patients(db: Session, query: str = "", skip: int = 0, limit: int = 100) -> tuple[int, list[models.Patient]]:
    query_lower = f"%{query.lower()}%"
    patients_query = db.query(models.Patient).filter(
        (func.lower(models.Patient.name).like(query_lower)) | (func.lower(models.Patient.nickname).like(query_lower))
    )
    total_count = patients_query.count()
    patients = patients_query.offset(skip).limit(limit).all()

    for p in patients:
        if p.encrypted_medical_history:
            p.medical_history = decrypt(p.encrypted_medical_history)
    return total_count, patients
