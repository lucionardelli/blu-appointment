from datetime import datetime, timedelta, timezone

from sqlalchemy import case
from sqlalchemy.orm import Session

from app.appointments.models import DayOfWeek
from app.payments import models as payment_models
from app.payments import schemas as payment_schemas
from app.patients.services import get_special_price
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
        # Check for a patient-specific price for this specialty
        special_price = get_special_price(db, appointment_in.patient_id, appointment_in.specialty_id)
        if special_price:
            cost = special_price.price
        else:
            # Fallback to the specialty's current price
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

    # Calculate the original duration before updating start_time
    original_duration = original_appointment.end_time - original_appointment.start_time

    original_appointment.start_time = new_start_time
    original_appointment.end_time = new_start_time + original_duration
    original_appointment.status = models.AppointmentStatus.RESCHEDULED

    db.add(original_appointment)
    db.commit()
    db.refresh(original_appointment)

    return original_appointment


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
        payment_method_id=payment_in.payment_method_id,
        patient_id=db_appointment.patient_id,
    )
    db.add(db_payment)

    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payments_for_appointment(db: Session, appointment_id: int) -> list[payment_models.Payment]:
    return (
        db.query(payment_models.Payment)
        .filter(payment_models.Payment.appointment_id == appointment_id)
        .order_by(payment_models.Payment.payment_date.desc())
        .all()
    )


def get_working_hours(db: Session) -> list[models.WorkingHours]:
    day_order = case(
        (models.WorkingHours.day_of_week == DayOfWeek.MONDAY, 1),
        (models.WorkingHours.day_of_week == DayOfWeek.TUESDAY, 2),
        (models.WorkingHours.day_of_week == DayOfWeek.WEDNESDAY, 3),
        (models.WorkingHours.day_of_week == DayOfWeek.THURSDAY, 4),
        (models.WorkingHours.day_of_week == DayOfWeek.FRIDAY, 5),
        (models.WorkingHours.day_of_week == DayOfWeek.SATURDAY, 6),
        (models.WorkingHours.day_of_week == DayOfWeek.SUNDAY, 7),
        else_=0,  # Default value if none of the conditions match
    )

    return db.query(models.WorkingHours).order_by(day_order).all()


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
