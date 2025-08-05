from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db import get_db
from . import schemas, crud

router = APIRouter()

# --- Appointments ---

@router.post("/", response_model=schemas.Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_appointment(db=db, appointment_in=appointment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{appointment_id}/cancel", response_model=schemas.Appointment)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = crud.cancel_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

@router.patch("/{appointment_id}/reschedule", response_model=schemas.Appointment)
def reschedule_appointment(
    appointment_id: int,
    new_start_time: datetime = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    db_appointment = crud.reschedule_appointment(db, appointment_id=appointment_id, new_start_time=new_start_time)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

# --- Payments ---

@router.post("/{appointment_id}/payments", response_model=schemas.Appointment)
def add_payment_to_appointment(
    appointment_id: int,
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db)
):
    db_appointment = crud.add_payment(db, appointment_id=appointment_id, payment_in=payment)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

# --- Working Hours ---

@router.get("/working-hours/", response_model=List[schemas.WorkingHours])
def get_working_hours(db: Session = Depends(get_db)):
    return crud.get_working_hours(db)

@router.post("/working-hours/", response_model=List[schemas.WorkingHours])
def set_working_hours(
    working_hours: List[schemas.WorkingHoursCreate],
    db: Session = Depends(get_db)
):
    return crud.set_working_hours(db, hours_in=working_hours)

# --- Recurring Appointments (Placeholder) ---

@router.post("/recurring/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def create_recurring_appointments(series: schemas.RecurringSeriesCreate, db: Session = Depends(get_db)):
    # This is a complex operation and will be implemented later.
    return {"detail": "Recurring appointment creation is not yet implemented."}
