from datetime import date, datetime
from typing import Annotated, Never

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.payments import schemas as payment_schemas
from app.patients import services as patient_services
from app.specialties import services as specialty_services
from app.specialties.rules import get_treatment_duration
from app.users.logged import get_current_user
from app.users.models import User

from . import metrics, models, schemas, services

appointments_router = APIRouter()
working_hours_router = APIRouter()
metrics_router = APIRouter()


@appointments_router.post("/", response_model=schemas.Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.Appointment:
    try:
        return services.create_appointment(db=db, appointment_in=appointment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@appointments_router.get("/", response_model=list[schemas.Appointment], status_code=status.HTTP_200_OK)
def get_appointments(
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    patient_id: int | None = None,
    status: Annotated[
        list[schemas.AppointmentStatus] | None,
        Query(description="Filter by appointment status. Can be specified multiple times."),
    ] = None,
    show_canceled: bool = False,
) -> list[schemas.Appointment]:
    return services.get_appointments(
        db=db,
        skip=skip,
        limit=limit,
        start_time=start_time,
        end_time=end_time,
        patient_id=patient_id,
        status=status,
        show_canceled=show_canceled,
    )


@appointments_router.get("/suggested-duration/")
def get_suggested_treatment_duration(
    patient_id: Annotated[int, Query(..., description="ID of the patient")],
    specialty_id: Annotated[int, Query(..., description="ID of the specialty")],
    before_time: Annotated[datetime, Query(default_factory=datetime.now, description="Consider appointments before this time")],
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    db_specialty = specialty_services.get_specialty_by_id(db, specialty_id=specialty_id)
    if not db_specialty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specialty not found")
    logic_key = db_specialty.treatment_duration_logic
    if not logic_key:
        return Response(status_code=204)

    db_patient = patient_services.get_patient(db, patient_id=patient_id)
    if not db_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    session_count = services.count_past_appointments_for_specialty(
        db,
        patient_id=patient_id,
        specialty_id=specialty_id,
        before_time=before_time,
    )
    return get_treatment_duration(logic_key, db_patient, session_count)


@appointments_router.post("/recurring/", status_code=status.HTTP_501_NOT_IMPLEMENTED, response_model=None)
def create_recurring_appointments(
    _series: schemas.RecurringSeriesCreate,
    _db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> Never:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Recurring appointments creation is not yet implemented."
    )


@appointments_router.get("/{appointment_id}/", response_model=schemas.Appointment)
def get_appointment(
    appointment_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.Appointment:
    db_appointment = services.get_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment


@appointments_router.put("/{appointment_id}/", response_model=schemas.Appointment)
def update_appointment(
    appointment_id: int,
    appointment_update: schemas.AppointmentUpdate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.Appointment:
    db_appointment = services.update_appointment(
        db, appointment_id=appointment_id, appointment_update=appointment_update
    )
    if db_appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment


@appointments_router.patch("/{appointment_id}/cancel/", response_model=schemas.Appointment)
def cancel_appointment(
    appointment_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.Appointment:
    db_appointment = services.cancel_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment


@appointments_router.patch("/{appointment_id}/restore/", response_model=schemas.Appointment)
def restore_appointment(
    appointment_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.Appointment:
    db_appointment = services.restore_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment


@appointments_router.delete("/{appointment_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(
    appointment_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    db_appointment = services.delete_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@appointments_router.patch("/{appointment_id}/reschedule/", response_model=schemas.Appointment)
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


@appointments_router.post("/{appointment_id}/payments/", response_model=payment_schemas.Payment)
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


@appointments_router.get("/{appointment_id}/payments/", response_model=list[payment_schemas.Payment])
def get_payments_for_appointment(
    appointment_id: int,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[models.Payment]:
    db_appointment = services.get_appointment(db, appointment_id=appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return services.get_payments_for_appointment(db, appointment_id=appointment_id)


@working_hours_router.get("/", response_model=list[schemas.WorkingHours])
def get_working_hours(
    db: Annotated[Session, Depends(get_db)], _current_user: Annotated[User, Depends(get_current_user)]
) -> list[schemas.WorkingHours]:
    return services.get_working_hours(db)


@working_hours_router.post("/", response_model=list[schemas.WorkingHours])
def set_working_hours(
    working_hours: list[schemas.WorkingHoursCreate],
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[schemas.WorkingHours]:
    return services.set_working_hours(db, hours_in=working_hours)


@metrics_router.get("/", response_model=schemas.AppointmentMetrics)
def get_appointment_metrics(
    start_date: Annotated[date, Query(description="Start time for the metrics")],
    end_date: Annotated[date, Query(description="End time for the metrics")],
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.AppointmentMetrics:
    return metrics.get_appointment_metrics(start_date=start_date, end_date=end_date, db=db)


@metrics_router.get("/dashboard/", response_model=schemas.DashboardMetrics)
def get_dashboard_metrics(
    db: Annotated[Session, Depends(get_db)], _current_user: Annotated[User, Depends(get_current_user)]
) -> schemas.DashboardMetrics:
    return metrics.get_dashboard_metrics(db=db)
