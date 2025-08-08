from datetime import date, datetime, timedelta
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


def get_dashboard_metrics(db: Session) -> schemas.DashboardMetrics:
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    # Appointments today
    appointments_today = (
        db.query(func.count(models.Appointment.id))
        .filter(
            and_(
                func.date(models.Appointment.start_time) == today,
                models.Appointment.status != "cancelled",
            )
        )
        .scalar()
    )

    # Appointments this week
    appointments_this_week = (
        db.query(func.count(models.Appointment.id))
        .filter(
            and_(
                models.Appointment.start_time >= start_of_week,
                models.Appointment.start_time < end_of_week,
                models.Appointment.status != "cancelled",
            )
        )
        .scalar()
    )

    # Revenue metrics for this month
    start_of_this_month = today.replace(day=1)
    # To get the end of this month, we get the first day of the next month and subtract one day
    next_month = (start_of_this_month + timedelta(days=32)).replace(day=1)
    end_of_this_month = next_month

    this_month_metrics = get_appointment_metrics(
        start_date=start_of_this_month, end_date=end_of_this_month, db=db
    )

    # Revenue metrics for last month
    end_of_last_month = start_of_this_month
    start_of_last_month = (end_of_last_month - timedelta(days=1)).replace(day=1)

    last_month_metrics = get_appointment_metrics(
        start_date=start_of_last_month, end_date=end_of_last_month, db=db
    )

    return schemas.DashboardMetrics(
        appointments_today=appointments_today,
        appointments_this_week=appointments_this_week,
        expected_revenue_this_month=this_month_metrics.total_revenue,
        expected_revenue_last_month=last_month_metrics.total_revenue,
        total_charged_this_month=this_month_metrics.total_charged,
        total_charged_last_month=last_month_metrics.total_charged,
        total_due_this_month=this_month_metrics.total_due,
        total_due_last_month=last_month_metrics.total_due,
    )
