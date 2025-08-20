import pytest
from app.patients import services as patient_services
from app.patients import schemas as patient_schemas
from app.users.models import User
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_patient(authenticated_client: TestClient, db_session: Session):
    response = authenticated_client.post(
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


def test_read_patients(authenticated_client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Jane Doe", email="jane.doe@example.com")
    patient_services.create_patient(db_session, patient_data)

    response = authenticated_client.get("/api/v1/patients/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Jane Doe"


def test_read_patient(authenticated_client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Jim Doe", email="jim.doe@example.com")
    patient = patient_services.create_patient(db_session, patient_data)

    response = authenticated_client.get(f"/api/v1/patients/{patient.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Jim Doe"
    assert data["id"] == patient.id


def test_update_patient(authenticated_client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Jill Doe", email="jill.doe@example.com")
    patient = patient_services.create_patient(db_session, patient_data)

    response = authenticated_client.put(
        f"/api/v1/patients/{patient.id}",
        json={"name": "Jill Smith"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Jill Smith"
    assert data["email"] == "jill.doe@example.com"


def test_delete_patient(authenticated_client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Jack Doe", email="jack.doe@example.com")
    patient = patient_services.create_patient(db_session, patient_data)

    response = authenticated_client.delete(f"/api/v1/patients/{patient.id}")
    assert response.status_code == status.HTTP_200_OK

    response = authenticated_client.get(f"/api/v1/patients/{patient.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_emergency_contact(test_user: User, authenticated_client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Patient for EC", email="ec@example.com")
    patient = patient_services.create_patient(db_session, patient_data)
    ice_qty_before_post = len(patient.emergency_contacts)

    response = authenticated_client.post(
        f"/api/v1/patients/{patient.id}/emergency_contacts",
        json={
            "full_name": "Emergency Contact 1",
            "patient_relationship": "Parent",
            "phone_number": "111-222-3333",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["full_name"] == "Emergency Contact 1"
    assert data["patient_id"] == patient.id
    assert data["priority"] == ice_qty_before_post + 1
    assert "id" in data


def test_read_emergency_contacts(authenticated_client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Patient for EC Read", email="ecread@example.com")
    patient = patient_services.create_patient(db_session, patient_data)

    authenticated_client.post(
        f"/api/v1/patients/{patient.id}/emergency_contacts",
        json={
            "full_name": "EC 1",
            "patient_relationship": "Sibling",
        },
    )
    authenticated_client.post(
        f"/api/v1/patients/{patient.id}/emergency_contacts",
        json={
            "full_name": "EC 2",
            "patient_relationship": "Friend",
        },
    )

    response = authenticated_client.get(f"/api/v1/patients/{patient.id}/emergency_contacts")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    # data is not ordered by priority in the response, so we check for presence
    assert any(contact["full_name"] == "EC 1" for contact in data)
    assert any(contact["full_name"] == "EC 2" for contact in data)


def test_read_single_emergency_contact(authenticated_client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Patient for EC Single", email="ecsingle@example.com")
    patient = patient_services.create_patient(db_session, patient_data)

    response = authenticated_client.post(
        f"/api/v1/patients/{patient.id}/emergency_contacts",
        json={
            "full_name": "EC Single",
            "patient_relationship": "Spouse",
            "priority": 1,
        },
    )
    contact_id = response.json()["id"]

    response = authenticated_client.get(f"/api/v1/patients/{patient.id}/emergency_contacts/{contact_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "EC Single"

    # Test 404 for non-existent contact
    response = authenticated_client.get(f"/api/v1/patients/{patient.id}/emergency_contacts/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test 404 for contact belonging to another patient
    other_patient_data = patient_schemas.PatientCreate(name="Other Patient", email="other@example.com")
    other_patient = patient_services.create_patient(db_session, other_patient_data)
    response = authenticated_client.post(
        f"/api/v1/patients/{other_patient.id}/emergency_contacts",
        json={
            "full_name": "EC Other",
            "patient_relationship": "Friend",
            "priority": 1,
        },
    )
    other_contact_id = response.json()["id"]

    response = authenticated_client.get(f"/api/v1/patients/{patient.id}/emergency_contacts/{other_contact_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_emergency_contact(test_user: User, authenticated_client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Patient for EC Update", email="ecupdate@example.com")
    patient = patient_services.create_patient(db_session, patient_data)

    response = authenticated_client.post(
        f"/api/v1/patients/{patient.id}/emergency_contacts",
        json={
            "full_name": "EC 1 Name",
            "patient_relationship": "Brother",
        },
    )
    contact_id_1 = response.json()["id"]

    response = authenticated_client.post(
        f"/api/v1/patients/{patient.id}/emergency_contacts",
        json={
            "full_name": "EC 2 Name",
            "patient_relationship": "Brother",
        },
    )
    contact_id_2 = response.json()["id"]
    contact_id_2_priority = response.json()["priority"]

    number_ice_contacts = len(patient.emergency_contacts)
    # Using a priority that is > #emergency contacts should raise an error
    with pytest.raises(ValueError):  # noqa: PT011
        authenticated_client.put(
            f"/api/v1/patients/{patient.id}/emergency_contacts/{contact_id_1}",
            json={
                "full_name": "EC 1 New Name",
                "priority": number_ice_contacts + 1,  # Invalid priority
            },
        )

    response = authenticated_client.put(
        f"/api/v1/patients/{patient.id}/emergency_contacts/{contact_id_2}",
        json={
            "full_name": "EC 2 New Name",
            "priority": contact_id_2_priority - 1,  # Valid priority
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "EC 2 New Name"
    assert data["priority"] == contact_id_2_priority - 1

    db_session.refresh(patient)
    updated_contacts = patient.emergency_contacts
    assert len(updated_contacts) == 2
    for contact in updated_contacts:
        if contact.id == contact_id_1:
            assert contact.priority == 2
        elif contact.id == contact_id_2:
            assert contact.full_name == "EC 2 New Name"
            assert contact.priority == 1


def test_delete_emergency_contact(authenticated_client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Patient for EC Delete", email="ecdelete@example.com")
    patient = patient_services.create_patient(db_session, patient_data)

    response = authenticated_client.post(
        f"/api/v1/patients/{patient.id}/emergency_contacts",
        json={
            "full_name": "EC to Delete",
            "patient_relationship": "Sister",
            "priority": 1,
        },
    )
    contact_id = response.json()["id"]

    response = authenticated_client.delete(f"/api/v1/patients/{patient.id}/emergency_contacts/{contact_id}")
    assert response.status_code == status.HTTP_200_OK

    response = authenticated_client.get(f"/api/v1/patients/{patient.id}/emergency_contacts/{contact_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_patient_details_includes_emergency_contacts(authenticated_client: TestClient, db_session: Session):
    patient_data = patient_schemas.PatientCreate(name="Patient with EC", email="patec@example.com")
    patient = patient_services.create_patient(db_session, patient_data)

    authenticated_client.post(
        f"/api/v1/patients/{patient.id}/emergency_contacts",
        json={
            "full_name": "EC A",
            "patient_relationship": "Friend",
            "priority": 2,
        },
    )
    authenticated_client.post(
        f"/api/v1/patients/{patient.id}/emergency_contacts",
        json={
            "full_name": "EC B",
            "patient_relationship": "Family",
            "priority": 1,
        },
    )

    response = authenticated_client.get(f"/api/v1/patients/{patient.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "emergency_contacts" in data
    assert len(data["emergency_contacts"]) == 2
    # Contacts are not ordered by priority in the response, so we check for presence
    assert any(contact["full_name"] == "EC A" for contact in data["emergency_contacts"])
    assert any(contact["full_name"] == "EC B" for contact in data["emergency_contacts"])
