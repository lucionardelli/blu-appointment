from datetime import date, datetime, timedelta, time, timezone

import pytest
from app.appointments import schemas as appointment_schemas
from app.appointments import services as appointment_services
from app.patients.schemas import PatientCreate
from app.patients.services import create_patient
from app.payments import schemas as payment_schemas
from app.specialties.schemas import SpecialtyCreate
from app.specialties.services import create_specialty
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def patient_in_db(db_session: Session):
    patient_data = PatientCreate(name="Test Patient", dob="1990-01-01", email="test@example.com")
    return create_patient(db_session, patient_data)


@pytest.fixture
def specialty_in_db(db_session: Session):
    specialty_data = SpecialtyCreate(name="Test Specialty", default_duration_minutes=30, current_price=100.00)
    return create_specialty(db_session, specialty_data)


@pytest.fixture
def cash_payment_method_in_db(db_session: Session):
    from app.payments.schemas import PaymentMethodCreate
    from app.payments.services import create_payment_method

    payment_method_data = PaymentMethodCreate(name="Cash", is_active=True)
    return create_payment_method(db_session, payment_method_data)


@pytest.fixture
def card_payment_method_in_db(db_session: Session):
    from app.payments.schemas import PaymentMethodCreate
    from app.payments.services import create_payment_method

    payment_method_data = PaymentMethodCreate(name="Card", is_active=True)
    return create_payment_method(db_session, payment_method_data)


def test_create_appointment(authenticated_client: TestClient, patient_in_db, specialty_in_db):
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(minutes=30)
    response = authenticated_client.post(
        "/api/v1/appointments/",
        json={
            "patient_id": patient_in_db.id,
            "specialty_id": specialty_in_db.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "cost": 100.00,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["patient"]["id"] == patient_in_db.id
    assert data["specialty"]["id"] == specialty_in_db.id
    assert "id" in data
    assert data["status"] == "SCHEDULED"


def test_create_appointment_auto_end_time_and_cost(authenticated_client: TestClient, patient_in_db, specialty_in_db):
    start_time = datetime.now() + timedelta(days=2)
    response = authenticated_client.post(
        "/api/v1/appointments/",
        json={
            "patient_id": patient_in_db.id,
            "specialty_id": specialty_in_db.id,
            "start_time": start_time.isoformat(),
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["cost"] == "100.00"  # Default price from specialty
    # Check if end_time is approximately start_time + default_duration_minutes
    expected_end_time = start_time + timedelta(minutes=specialty_in_db.default_duration_minutes)
    assert datetime.fromisoformat(data["end_time"]).minute == expected_end_time.minute
    assert datetime.fromisoformat(data["end_time"]).hour == expected_end_time.hour


def test_create_appointment_invalid_patient_or_specialty(authenticated_client: TestClient):
    start_time = datetime.now() + timedelta(days=1)
    response = authenticated_client.post(
        "/api/v1/appointments/",
        json={
            "patient_id": 99999,  # Non-existent patient
            "specialty_id": 1,
            "start_time": start_time.isoformat(),
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = authenticated_client.post(
        "/api/v1/appointments/",
        json={
            "patient_id": 1,
            "specialty_id": 99999,  # Non-existent specialty
            "start_time": start_time.isoformat(),
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_appointments(authenticated_client: TestClient, patient_in_db, specialty_in_db, db_session: Session):
    # Create a few appointments
    app1_start = datetime.now() + timedelta(days=3)
    app2_start = datetime.now() + timedelta(days=4)
    appointment_services.create_appointment(
        db_session,
        appointment_schemas.AppointmentCreate(
            patient_id=patient_in_db.id,
            specialty_id=specialty_in_db.id,
            start_time=app1_start,
            end_time=app1_start + timedelta(minutes=30),
        ),
    )
    appointment_services.create_appointment(
        db_session,
        appointment_schemas.AppointmentCreate(
            patient_id=patient_in_db.id,
            specialty_id=specialty_in_db.id,
            start_time=app2_start,
            end_time=app2_start + timedelta(minutes=30),
        ),
    )

    response = authenticated_client.get("/api/v1/appointments/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2  # May contain other appointments from other tests if not properly isolated

    # Test filtering by status (e.g., "scheduled")
    response = authenticated_client.get("/api/v1/appointments/?status=SCHEDULED")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert all(app["status"] == "SCHEDULED" for app in data)


def test_get_appointment(authenticated_client: TestClient, patient_in_db, specialty_in_db, db_session: Session):
    start_time = datetime.now() + timedelta(days=5)
    appointment = appointment_services.create_appointment(
        db_session,
        appointment_schemas.AppointmentCreate(
            patient_id=patient_in_db.id,
            specialty_id=specialty_in_db.id,
            start_time=start_time,
            end_time=start_time + timedelta(minutes=30),
        ),
    )

    response = authenticated_client.get(f"/api/v1/appointments/{appointment.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == appointment.id
    assert data["patient"]["id"] == patient_in_db.id
    assert data["specialty"]["id"] == specialty_in_db.id


def test_get_appointment_not_found(authenticated_client: TestClient):
    response = authenticated_client.get("/api/v1/appointments/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_appointment(authenticated_client: TestClient, patient_in_db, specialty_in_db, db_session: Session):
    start_time = datetime.now() + timedelta(days=6)
    end_time = start_time + timedelta(minutes=30)
    appointment = appointment_services.create_appointment(
        db_session,
        appointment_schemas.AppointmentCreate(
            patient_id=patient_in_db.id,
            specialty_id=specialty_in_db.id,
            start_time=start_time,
            end_time=end_time,
        ),
    )

    new_start_time = start_time + timedelta(hours=1)
    new_end_time = end_time + timedelta(hours=1)
    response = authenticated_client.put(
        f"/api/v1/appointments/{appointment.id}",
        json={
            "start_time": new_start_time.isoformat(),
            "end_time": new_end_time.isoformat(),
            "cost": 150.00,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == appointment.id
    assert data["cost"] == "150.00"
    assert datetime.fromisoformat(data["start_time"]).hour == new_start_time.hour


def test_update_appointment_not_found(authenticated_client: TestClient):
    start_time = datetime.now() + timedelta(days=6)
    response = authenticated_client.put(
        "/api/v1/appointments/99999",
        json={
            "start_time": start_time.isoformat(),
            "end_time": (start_time + timedelta(minutes=30)).isoformat(),
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_cancel_appointment(authenticated_client: TestClient, patient_in_db, specialty_in_db, db_session: Session):
    start_time = datetime.now() + timedelta(days=7)
    appointment = appointment_services.create_appointment(
        db_session,
        appointment_schemas.AppointmentCreate(
            patient_id=patient_in_db.id,
            specialty_id=specialty_in_db.id,
            start_time=start_time,
            end_time=start_time + timedelta(minutes=30),
        ),
    )

    response = authenticated_client.patch(f"/api/v1/appointments/{appointment.id}/cancel")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == appointment.id
    assert data["status"] == "CANCELLED"


def test_cancel_appointment_not_found(authenticated_client: TestClient):
    response = authenticated_client.patch("/api/v1/appointments/99999/cancel")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_reschedule_appointment(authenticated_client: TestClient, patient_in_db, specialty_in_db, db_session: Session):
    start_time = datetime.now() + timedelta(days=8)
    appointment = appointment_services.create_appointment(
        db_session,
        appointment_schemas.AppointmentCreate(
            patient_id=patient_in_db.id,
            specialty_id=specialty_in_db.id,
            start_time=start_time,
            end_time=start_time + timedelta(minutes=30),
        ),
    )

    new_start_time = (datetime.now() + timedelta(days=9, hours=1)).replace(tzinfo=timezone.utc)
    response = authenticated_client.patch(
        f"/api/v1/appointments/{appointment.id}/reschedule",
        json={"new_start_time": new_start_time.isoformat()},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == appointment.id
    assert datetime.fromisoformat(data["start_time"]).hour == new_start_time.hour
    assert datetime.fromisoformat(data["end_time"]) == (new_start_time + timedelta(minutes=30)).replace(tzinfo=timezone.utc)


def test_reschedule_appointment_not_found(authenticated_client: TestClient):
    new_start_time = datetime.now() + timedelta(days=9, hours=1)
    response = authenticated_client.patch(
        "/api/v1/appointments/99999/reschedule",
        json={"new_start_time": new_start_time.isoformat()},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_add_payment_to_appointment(
        authenticated_client: TestClient, patient_in_db, specialty_in_db, db_session: Session, payment_method_in_db
    ):
    start_time = datetime.now() + timedelta(days=10)
    appointment = appointment_services.create_appointment(
        db_session,
        appointment_schemas.AppointmentCreate(
            patient_id=patient_in_db.id,
            specialty_id=specialty_in_db.id,
            start_time=start_time,
            end_time=start_time + timedelta(minutes=30),
            cost=200.00,
        ),
    )

    response = authenticated_client.post(
        f"/api/v1/appointments/{appointment.id}/payments",
        json={"amount": 50.00, "payment_method_id": payment_method_in_db.id, "patient_id": patient_in_db.id},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["amount"] == "50.00"
    assert data["payment_method"]["name"] == payment_method_in_db.name
    assert "id" in data
    assert "payment_date" in data

    # Verify total_paid is updated on the appointment
    updated_appointment = appointment_services.get_appointment(db_session, appointment.id)
    assert updated_appointment.total_paid == 50.00


def test_add_payment_to_appointment_not_found(authenticated_client: TestClient):
    response = authenticated_client.post(
        "/api/v1/appointments/99999/payments",
        json={"amount": 50.00, "payment_method_id": 1, "patient_id": 1},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_payments_for_appointment(
    authenticated_client: TestClient,
    patient_in_db,
    specialty_in_db,
    cash_payment_method_in_db,
    card_payment_method_in_db,
    db_session: Session,
):
    start_time = datetime.now() + timedelta(days=11)

    appointment = appointment_services.create_appointment(
        db_session,
        appointment_schemas.AppointmentCreate(
            patient_id=patient_in_db.id,
            specialty_id=specialty_in_db.id,
            start_time=start_time,
            end_time=start_time + timedelta(minutes=30),
            cost=200.00,
        ),
    )

    payment_response = authenticated_client.post(
        f"/api/v1/appointments/{appointment.id}/payments",
        json={
            "amount": 50.00,
            "payment_method_id": cash_payment_method_in_db.id,
            "patient_id": patient_in_db.id,
        },
    )
    assert payment_response.status_code == status.HTTP_200_OK

    payment_response = authenticated_client.post(
        f"/api/v1/appointments/{appointment.id}/payments",
        json={
            "amount": 75.00,
            "payment_method_id": card_payment_method_in_db.id,
            "patient_id": patient_in_db.id,
        },
    )
    assert payment_response.status_code == status.HTTP_200_OK

    response = authenticated_client.get(f"/api/v1/appointments/{appointment.id}/payments")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert any(p["amount"] == "50.00" for p in data)
    assert any(p["amount"] == "75.00" for p in data)


def test_get_payments_for_appointment_not_found(authenticated_client: TestClient):
    response = authenticated_client.get("/api/v1/appointments/99999/payments")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_working_hours(authenticated_client: TestClient):
    response = authenticated_client.get("/api/v1/working-hours/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_set_working_hours(authenticated_client: TestClient):
    working_hours_data = [
        {"dayOfWeek": "Monday", "startTime": time(9, 0, 0).isoformat(), "endTime": time(17, 0, 0).isoformat()},
        {"dayOfWeek": "Tuesday", "is_closed": True},
    ]
    response = authenticated_client.post("/api/v1/working-hours/", json=working_hours_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["dayOfWeek"] == "Monday"
    assert data[0]["startTime"] == "09:00:00"
    assert data[1]["is_closed"] is True


def test_set_working_hours_invalid_data(authenticated_client: TestClient):
    # Invalid: is_closed is true but times are provided
    invalid_data = [{"dayOfWeek": 0, "startTime": "09:00:00", "endTime": "17:00:00", "is_closed": True}]
    response = authenticated_client.post("/api/v1/working-hours/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Invalid: start_time after end_time
    invalid_data = [{"dayOfWeek": 0, "startTime": "17:00:00", "endTime": "09:00:00"}]
    response = authenticated_client.post("/api/v1/working-hours/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_recurring_appointments_not_implemented(authenticated_client: TestClient):
    response = authenticated_client.post(
        "/api/v1/appointments/recurring/",
        json={
            "patient_id": 1,
            "specialty_id": 1,
            "start_time": datetime.now().isoformat(),
            "frequency": "WEEKLY",
            "number_of_appointments": 5,
        },
    )
    assert response.status_code == status.HTTP_501_NOT_IMPLEMENTED
    assert response.json() == {"detail": "Recurring appointments creation is not yet implemented."}


def test_create_recurring_appointments_schema_validation(authenticated_client: TestClient):
    # Test case: neither end_date nor number_of_appointments provided
    response = authenticated_client.post(
        "/api/v1/appointments/recurring/",
        json={
            "patient_id": 1,
            "specialty_id": 1,
            "start_time": datetime.now().isoformat(),
            "frequency": "WEEKLY",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Either end_date or number_of_appointments must be provided." in str(response.json())

    # Test case: both end_date and number_of_appointments provided
    response = authenticated_client.post(
        "/api/v1/appointments/recurring/",
        json={
            "patient_id": 1,
            "specialty_id": 1,
            "start_time": datetime.now().isoformat(),
            "frequency": "WEEKLY",
            "end_date": date.today().isoformat(),
            "number_of_appointments": 5,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Only one of end_date or number_of_appointments should be provided." in str(response.json())


def test_get_appointment_metrics(authenticated_client: TestClient, patient_in_db, specialty_in_db, db_session: Session, payment_method_in_db):
    # Create some appointments for metrics
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # Appointment within the period
    appointment_services.create_appointment(
        db_session,
        appointment_schemas.AppointmentCreate(
            patient_id=patient_in_db.id,
            specialty_id=specialty_in_db.id,
            start_time=datetime.combine(today, datetime.min.time()),
            end_time=datetime.combine(today, datetime.min.time()) + timedelta(minutes=30),
            cost=100.00,
        ),
    )
    # Another appointment within the period, partially paid
    app2 = appointment_services.create_appointment(
        db_session,
        appointment_schemas.AppointmentCreate(
            patient_id=patient_in_db.id,
            specialty_id=specialty_in_db.id,
            start_time=datetime.combine(today, datetime.min.time()) + timedelta(hours=1),
            end_time=datetime.combine(today, datetime.min.time()) + timedelta(hours=1, minutes=30),
            cost=200.00,
        ),
    )
    appointment_services.add_payment(db_session, appointment_id=app2.id, payment_in=payment_schemas.PaymentCreate(amount=50.00, payment_method_id=payment_method_in_db.id, patient_id=app2.patient_id))

    # Appointment outside the period (yesterday)
    appointment_services.create_appointment(
        db_session,
        appointment_schemas.AppointmentCreate(
            patient_id=patient_in_db.id,
            specialty_id=specialty_in_db.id,
            start_time=datetime.combine(yesterday, datetime.min.time()),
            end_time=datetime.combine(yesterday, datetime.min.time()) + timedelta(minutes=30),
            cost=50.00,
        ),
    )

    response = authenticated_client.get(
        f"/api/v1/metrics/?start_date={today.isoformat()}&end_date={tomorrow.isoformat()}"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_appointments"] == 2
    assert data["total_charged"] == "50.00"
    assert data["total_revenue"] == "300.00"
    assert data["total_due"] == "250.00"
    assert data["period_start"] == today.isoformat()
    assert data["period_end"] == tomorrow.isoformat()


def test_get_dashboard_metrics(authenticated_client: TestClient, patient_in_db, specialty_in_db, db_session: Session):
    # This test will be more complex as it depends on current date/time
    # For simplicity, we'll just check if the endpoint returns a 200 OK and the expected keys
    response = authenticated_client.get("/api/v1/metrics/dashboard/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "appointments_today" in data
    assert "appointments_this_week" in data
    assert "expected_revenue_last_month" in data
    assert "expected_revenue_this_month" in data
    assert "total_charged_last_month" in data
    assert "total_charged_this_month" in data
    assert "total_due_last_month" in data
    assert "total_due_this_month" in data
