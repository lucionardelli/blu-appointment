from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.patients.models import Patient
from app.specialties.crud import get_current_price_for_specialty, get_specialty_by_id

from . import models, schemas


def create_appointment(
    db: Session,
    appointment_in: schemas.AppointmentCreate,
) -> models.Appointment:
    specialty = get_specialty_by_id(db, appointment_in.specialty_id)
    if not specialty:
        msg = "Specialty not found"
        raise ValueError(msg)

    cost = appointment_in.cost
    if cost is None:
        current_price = get_current_price_for_specialty(db, appointment_in.specialty_id)
        if current_price is None:
            msg = "Cannot create appointment: Specialty has no price defined."
            raise ValueError(
                msg,
            )
        cost = current_price

    end_time = appointment_in.start_time + timedelta(
        minutes=specialty.default_duration_minutes,
    )

    db_appointment = models.Appointment(
        patient_id=appointment_in.patient_id,
        specialty_id=appointment_in.specialty_id,
        start_time=appointment_in.start_time,
        end_time=end_time,
        cost=cost,
        status=models.AppointmentStatus.SCHEDULED,
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def cancel_appointment(db: Session, appointment_id: int) -> models.Appointment | None:
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        return None

    db_appointment.status = models.AppointmentStatus.CANCELLED
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def reschedule_appointment(
    db: Session,
    appointment_id: int,
    new_start_time: datetime,
) -> models.Appointment | None:
    original_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not original_appointment:
        return None

    # Create the new appointment based on the original
    new_appointment_data = schemas.AppointmentCreate(
        patient_id=original_appointment.patient_id,
        specialty_id=original_appointment.specialty_id,
        start_time=new_start_time,
        # Cost will be the current default
    )
    new_appointment = create_appointment(db, new_appointment_data)

    # Update the original appointment
    original_appointment.status = models.AppointmentStatus.RESCHEDULED
    original_appointment.rescheduled_to_appointment_id = new_appointment.id
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


# --- Payment CRUD ---


def add_payment(
    db: Session,
    appointment_id: int,
    payment_in: schemas.PaymentCreate,
) -> models.Appointment | None:
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        return None

    db_payment = models.Payment(
        appointment_id=appointment_id,
        amount=payment_in.amount,
        method=payment_in.method,
    )
    db.add(db_payment)

    # If patient credit was used, update the patient's balance
    if payment_in.method == models.PaymentMethod.PATIENT_CREDIT:
        patient = db.query(Patient).filter(Patient.id == db_appointment.patient_id).first()
        if patient:
            patient.credit_balance -= payment_in.amount

    db.commit()
    db.refresh(db_appointment)
    return db_appointment


# --- Working Hours CRUD ---


def get_working_hours(db: Session) -> list[models.WorkingHours]:
    return db.query(models.WorkingHours).order_by(models.WorkingHours.day_of_week).all()


def set_working_hours(
    db: Session,
    hours_in: list[schemas.WorkingHoursCreate],
) -> list[models.WorkingHours]:
    # Clear existing hours
    db.query(models.WorkingHours).delete()

    db_hours = []
    for hour_data in hours_in:
        db_hour = models.WorkingHours(**hour_data.model_dump())
        db.add(db_hour)
        db_hours.append(db_hour)

    db.commit()
    return get_working_hours(db)  # Return the newly saved hours
