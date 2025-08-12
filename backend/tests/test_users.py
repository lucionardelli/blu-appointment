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


def test_update_user_success(client: TestClient, db_session: Session):
    # Create a user to update
    response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "password": "testpassword123"},
    )
    # Authenticate the user to update their own information
    client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpassword123"},
    )

    # Update the user's first name and last name
    response = client.put("/api/v1/users/", json={"name": "Updated", "last_name": "User"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated"
    assert data["last_name"] == "User"


def test_update_username_is_not_allowed(client: TestClient, db_session: Session):
    # Create a user to update
    response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "password": "testpassword123"},
    )

    # Authenticate the user to update their own information
    client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpassword123"},
    )

    # Attempt to update the username
    response = client.put("/api/v1/users/", json={"username": "newusername"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_user_password_success(client: TestClient, db_session: Session):
    # Create a user to update
    response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "password": "testpassword123"},
    )

    # Authenticate the user to update their own information
    client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpassword123"},
    )

    # Update the user's password
    response = client.put(
        "/api/v1/users/password", json={"old_password": "testpassword123", "new_password": "newpassword456"}
    )
    assert response.status_code == status.HTTP_200_OK

    # Logout the user
    client.post("/api/v1/auth/logout")

    # Verify that the user can log in with the new password
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "newpassword456"},
    )
    assert response.status_code == status.HTTP_200_OK
