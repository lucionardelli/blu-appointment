from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.specialties import crud as specialty_crud
from app.specialties import schemas as specialty_schemas


def test_create_specialty(client: TestClient, db_session: Session):
    response = client.post(
        "/api/v1/specialties/",
        json={
            "name": "Psychology",
            "default_duration_minutes": 45,
            "current_price": 100.00,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Psychology"
    assert len(data["prices"]) == 1
    assert data["prices"][0]["price"] == "100.00"


def test_read_specialties(client: TestClient, db_session: Session):
    specialty_data = specialty_schemas.SpecialtyCreate(
        name="BluRoom",
        default_duration_minutes=20,
        current_price=50.00,
    )
    specialty_crud.create_specialty(db_session, specialty_data)

    response = client.get("/api/v1/specialties/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "BluRoom"
    assert data[0]["default_duration_minutes"] == 20
    assert data[0]["current_price"] == "50.00"


def test_update_specialty(client: TestClient, db_session: Session):
    specialty_data = specialty_schemas.SpecialtyCreate(
        name="Therapy",
        default_duration_minutes=60,
        current_price=120.00,
    )
    specialty = specialty_crud.create_specialty(db_session, specialty_data)

    response = client.put(
        f"/api/v1/specialties/{specialty.id}",
        json={"default_duration_minutes": 55},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Therapy"
    assert data["default_duration_minutes"] == 55


def test_add_new_specialty_price(client: TestClient, db_session: Session):
    specialty_data = specialty_schemas.SpecialtyCreate(
        name="Consultation",
        default_duration_minutes=30,
        current_price=75.00,
    )
    specialty = specialty_crud.create_specialty(db_session, specialty_data)

    response = client.post(
        f"/api/v1/specialties/{specialty.id}/prices",
        json={"price": 80.00},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["prices"]) == 2

    # Check that the new price is the latest one
    prices = sorted(data["prices"], key=lambda x: x["valid_from"], reverse=True)
    assert prices[0]["price"] == "80.00"
