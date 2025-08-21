from datetime import date, datetime
from typing import Annotated, Never

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.users.logged import get_current_user
from app.db.base import get_db
from app.users.models import User
from app.specialties.rules import get_treatment_duration

from . import services, metrics, models, schemas
from app.payments import schemas as payment_schemas

router = APIRouter()


@router.post("/", response_model=schemas.Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.Appointment:
    try:
        return services.create_appointment(db=db, appointment_in=appointment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/", response_model=list[schemas.Appointment], status_code=status.HTTP_200_OK)
def get_appointments(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
    user_id: int | None = None,
    status: Annotated[
        list[schemas.AppointmentStatus] | None,
        Query(description="Filter by appointment status. Can be specified multiple times."),
    ] = None,
    _current_user: Annotated[User, Depends(get_current_user)] = None,
) -> list[schemas.Appointment]:
    return services.get_appointments(db=db, skip=skip, limit=limit, user_id=user_id, status=status)


@router.get("/{appointment_id}", response_model=schemas.Appointment)
def get_appointment(
    appointment_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.Appointment:
    db_appointment = services.get_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")

    logic_key = db_appointment.specialty.treatment_duration_logic
    if logic_key:
        session_count = services.count_past_appointments_for_specialty(
            db,
            patient_id=db_appointment.patient_id,
            specialty_id=db_appointment.specialty_id,
            before_time=db_appointment.start_time,
        )
        duration = get_treatment_duration(logic_key, db_appointment.patient, session_count)
        # This dynamically added attribute will be picked up by the Pydantic model
        db_appointment.suggested_treatment_duration_minutes = duration

    return db_appointment


@router.put("/{appointment_id}", response_model=schemas.Appointment)
def update_appointment(
    appointment_id: int,
    appointment_update: schemas.AppointmentUpdate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.Appointment:
    db_appointment = services.update_appointment(db, appointment_id=appointment_id, appointment_update=appointment_update)
    if db_appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment


@router.patch("/{appointment_id}/cancel", response_model=schemas.Appointment)
def cancel_appointment(
    appointment_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.Appointment:
    db_appointment = services.cancel_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment


@router.patch("/{appointment_id}/reschedule", response_model=schemas.Appointment)
def reschedule_appointment(
    appointment_id: int,
    new_start_time: Annotated[datetime, Body(embed=True)],
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.Appointment:
    db_appointment = services.reschedule_appointment(db, appointment_id=appointment_id, new_start_time=new_start_time)
    if db_appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment


@router.post("/{appointment_id}/payments", response_model=payment_schemas.Payment)
def add_payment_to_appointment(
    appointment_id: int,
    payment: payment_schemas.PaymentCreate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> models.Payment:
    db_appointment = services.get_appointment(db, appointment_id=appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return services.add_payment(db, appointment_id=appointment_id, payment_in=payment)


@router.get("/{appointment_id}/payments", response_model=list[payment_schemas.Payment])
def get_payments_for_appointment(
    appointment_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[models.Payment]:
    db_appointment = services.get_appointment(db, appointment_id=appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return services.get_payments_for_appointment(db, appointment_id=appointment_id)


@router.get("/working-hours/", response_model=list[schemas.WorkingHours])
def get_working_hours(
    db: Annotated[Session, Depends(get_db)], _current_user: Annotated[User, Depends(get_current_user)]
) -> list[schemas.WorkingHours]:
    return services.get_working_hours(db)


@router.post("/working-hours/", response_model=list[schemas.WorkingHours])
def set_working_hours(
    working_hours: list[schemas.WorkingHoursCreate],
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[schemas.WorkingHours]:
    return services.set_working_hours(db, hours_in=working_hours)


@router.post("/recurring/", status_code=status.HTTP_501_NOT_IMPLEMENTED, response_model=None)
def create_recurring_appointments(
    _series: schemas.RecurringSeriesCreate,
    _db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> Never:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Recurring appointments creation is not yet implemented."
    )


@router.get("/metrics/", response_model=schemas.AppointmentMetrics)
def get_appointment_metrics(
    start_date: Annotated[date, Query(description="Start time for the metrics")],
    end_date: Annotated[date, Query(description="End time for the metrics")],
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.AppointmentMetrics:
    return metrics.get_appointment_metrics(start_date=start_date, end_date=end_date, db=db)


@router.get("/metrics/dashboard/", response_model=schemas.DashboardMetrics)
def get_dashboard_metrics(
    db: Annotated[Session, Depends(get_db)], _current_user: Annotated[User, Depends(get_current_user)]
) -> schemas.DashboardMetrics:
    return metrics.get_dashboard_metrics(db=db)
