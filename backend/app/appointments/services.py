from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.payments import models as payment_models
from app.payments import schemas as payment_schemas
from app.specialties.services import get_current_price_for_specialty, get_specialty_by_id

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

    end_time = appointment_in.end_time or appointment_in.start_time + timedelta(
        minutes=specialty.default_duration_minutes
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


def restore_appointment(db: Session, appointment_id: int) -> models.Appointment | None:
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        return None

    if db_appointment.status != models.AppointmentStatus.CANCELLED:
        msg = "Only cancelled appointments can be deleted."
        raise ValueError(msg)

    if db_appointment.start_time < datetime.now(tz=db_appointment.start_time.tzinfo):
        db_appointment.status = models.AppointmentStatus.COMPLETED
    else:
        db_appointment.status = models.AppointmentStatus.SCHEDULED
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def delete_appointment(db: Session, appointment_id: int) -> models.Appointment | None:
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        return None
    if db_appointment.status != models.AppointmentStatus.CANCELLED:
        msg = "Only cancelled appointments can be deleted."
        raise ValueError(msg)

    db.delete(db_appointment)
    db.commit()
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


def get_appointments(  # noqa: PLR0913
    db: Session,
    skip: int = 0,
    limit: int = 100,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    patient_id: int | None = None,
    status: list[models.AppointmentStatus] | None = None,
) -> list[models.Appointment]:
    """Get appointments with patient and specialty data for calendar display"""
    base_query = db.query(models.Appointment)

    if patient_id is not None:
        base_query = base_query.filter(models.Appointment.patient_id == patient_id)
    if status is not None:
        base_query = base_query.filter(models.Appointment.status.in_(status))
    if start_time is not None:
        base_query = base_query.filter(models.Appointment.start_time >= start_time)
    if end_time is not None:
        base_query = base_query.filter(models.Appointment.end_time <= end_time)

    return base_query.order_by(models.Appointment.start_time).offset(skip).limit(limit).all()


def get_appointment(db: Session, appointment_id: int) -> models.Appointment | None:
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()


def count_past_appointments_for_specialty(
    db: Session, patient_id: int, specialty_id: int, before_time: datetime
) -> int:
    """Counts the number of past appointments for a given patient and specialty."""
    return (
        db.query(models.Appointment)
        .filter(
            models.Appointment.patient_id == patient_id,
            models.Appointment.specialty_id == specialty_id,
            models.Appointment.start_time < before_time,
            models.Appointment.status != models.AppointmentStatus.CANCELLED,
        )
        .count()
    )


def update_appointment(
    db: Session,
    appointment_id: int,
    appointment_update: schemas.AppointmentUpdate,
) -> models.Appointment | None:
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        return None

    db_appointment.start_time = appointment_update.start_time
    db_appointment.end_time = appointment_update.end_time
    if appointment_update.cost is not None:
        db_appointment.cost = appointment_update.cost
    if appointment_update.status is not None:
        db_appointment.status = appointment_update.status

    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def add_payment(
    db: Session,
    appointment_id: int,
    payment_in: payment_schemas.PaymentCreate,
) -> payment_models.Payment:
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        return None

    db_payment = payment_models.Payment(
        appointment_id=appointment_id,
        amount=payment_in.amount,
        method=payment_in.method,
    )
    db.add(db_payment)

    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payments_for_appointment(db: Session, appointment_id: int) -> list[payment_models.Payment]:
    return db.query(payment_models.Payment).filter(payment_models.Payment.appointment_id == appointment_id).all()


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
