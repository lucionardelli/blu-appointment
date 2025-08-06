from datetime import datetime
from typing import Annotated, Never

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db

from . import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment: schemas.AppointmentCreate, db: Annotated[Session, Depends(get_db)]
) -> schemas.Appointment:
    try:
        return crud.create_appointment(db=db, appointment_in=appointment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

@router.get("/", response_model=list[schemas.Appointment], status_code=status.HTTP_200_OK)
def get_appointments(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
    user_id: int | None = None,
    status: list[schemas.AppointmentStatus] | None = None,
) -> list[schemas.Appointment]:
    return crud.get_appointments(db=db, skip=skip, limit=limit, user_id=user_id, status=status)

@router.patch("/{appointment_id}/cancel", response_model=schemas.Appointment)
def cancel_appointment(appointment_id: int, db: Annotated[Session, Depends(get_db)]) -> schemas.Appointment:
    db_appointment = crud.cancel_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment


@router.patch("/{appointment_id}/reschedule", response_model=schemas.Appointment)
def reschedule_appointment(
    appointment_id: int,
    new_start_time: Annotated[datetime, Body(embed=True)],
    db: Annotated[Session, Depends(get_db)],
) -> schemas.Appointment:
    db_appointment = crud.reschedule_appointment(db, appointment_id=appointment_id, new_start_time=new_start_time)
    if db_appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment


@router.post("/{appointment_id}/payments", response_model=schemas.Appointment)
def add_payment_to_appointment(
    appointment_id: int,
    payment: schemas.PaymentCreate,
    db: Annotated[Session, Depends(get_db)],
) -> schemas.Appointment:
    db_appointment = crud.add_payment(db, appointment_id=appointment_id, payment_in=payment)
    if db_appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return db_appointment


@router.get("/working-hours/", response_model=list[schemas.WorkingHours])
def get_working_hours(db: Annotated[Session, Depends(get_db)]) -> list[schemas.WorkingHours]:
    return crud.get_working_hours(db)


@router.post("/working-hours/", response_model=list[schemas.WorkingHours])
def set_working_hours(
    working_hours: list[schemas.WorkingHoursCreate],
    db: Annotated[Session, Depends(get_db)],
) -> list[schemas.WorkingHours]:
    return crud.set_working_hours(db, hours_in=working_hours)


@router.post("/recurring/", status_code=status.HTTP_501_NOT_IMPLEMENTED, response_model=None)
def create_recurring_appointments(
    series: schemas.RecurringSeriesCreate,  # noqa: ARG001
    db: Annotated[Session, Depends(get_db)],  # noqa: ARG001
) -> Never:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Recurring appointments creation is not yet implemented."
    )
