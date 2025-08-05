from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_user_success(client: TestClient, db_session: Session):
    response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "password": "testpassword123", "default_timezone": "UTC"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "hashed_password" not in data


def test_create_user_duplicate_username(client: TestClient, db_session: Session):
    # Create the first user
    client.post(
        "/api/v1/users/",
        json={"username": "testuser", "password": "testpassword123"},
    )

    # Attempt to create a second user with the same username
    response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "password": "anotherpassword"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Username already registered"}
