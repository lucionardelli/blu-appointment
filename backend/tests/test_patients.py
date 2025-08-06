from app.patients import crud as patient_crud
from app.patients import schemas as patient_schemas
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_patient(client: TestClient, db_session: Session):
    response = client.post(
        "/api/v1/patients/",
        json={
            "name": "John Doe",
            "dob": "1990-01-01",
            "medical_history": "Initial consultation.",
            "email": "john.doe@example.com",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john.doe@example.com"
    assert "id" in data


def test_read_patients(client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Jane Doe", email="jane.doe@example.com")
    patient_crud.create_patient(db_session, patient_data)

    response = client.get("/api/v1/patients/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Jane Doe"


def test_read_patient(client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Jim Doe", email="jim.doe@example.com")
    patient = patient_crud.create_patient(db_session, patient_data)

    response = client.get(f"/api/v1/patients/{patient.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Jim Doe"
    assert data["id"] == patient.id


def test_update_patient(client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Jill Doe", email="jill.doe@example.com")
    patient = patient_crud.create_patient(db_session, patient_data)

    response = client.put(
        f"/api/v1/patients/{patient.id}",
        json={"name": "Jill Smith"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Jill Smith"
    assert data["email"] == "jill.doe@example.com"


def test_delete_patient(client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Jack Doe", email="jack.doe@example.com")
    patient = patient_crud.create_patient(db_session, patient_data)

    response = client.delete(f"/api/v1/patients/{patient.id}")
    assert response.status_code == status.HTTP_200_OK

    response = client.get(f"/api/v1/patients/{patient.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
