from datetime import date
from decimal import Decimal

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from . import models, schemas


def get_appointment_metrics(
    *,
    start_date: date,
    end_date: date,
    db: Session,
) -> schemas.AppointmentMetrics:
    if start_date >= end_date:
        raise ValueError("start_date must be before end_date")

    # Build base filter conditions
    time_filter = and_(
        models.Appointment.start_time >= start_date,
        models.Appointment.start_time < end_date,
    )

    # Single query to get all appointment metrics at once
    metrics_query = db.query(
        func.count(models.Appointment.id).label("total_appointments"),
        func.coalesce(func.sum(models.Appointment.cost), 0).label("total_revenue"),
    ).filter(time_filter)

    result = metrics_query.first()
    total_appointments = result.total_appointments
    total_revenue = Decimal(str(result.total_revenue))

    # Get total charged amount with proper join
    charged_query = (
        db.query(func.coalesce(func.sum(models.Payment.amount), 0))
        .select_from(models.Appointment)
        .join(models.Payment, models.Payment.appointment_id == models.Appointment.id)
        .filter(time_filter)
    )

    total_charged = Decimal(str(charged_query.scalar() or 0))
    total_due = total_revenue - total_charged

    return schemas.AppointmentMetrics(
        total_appointments=total_appointments,
        total_revenue=total_revenue,
        total_charged=total_charged,
        total_due=total_due,
        period_start=start_date,
        period_end=end_date,
    )
