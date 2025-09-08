from app.core.security import verify_password
from app.users.models import User
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.conftest import TEST_USER_RAW_PASS


def test_create_user_success(authenticated_client: TestClient, db_session: Session):
    response = authenticated_client.post(
        "/api/v1/users/",
        json={"username": "testuser", "password": "testpassword123", "default_timezone": "UTC"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "hashed_password" not in data


def test_create_user_duplicate_username(test_user: User, authenticated_client: TestClient, db_session: Session):
    # Attempt to create a second user with the username of the test user
    response = authenticated_client.post(
        "/api/v1/users/",
        json={"username": test_user.username, "password": "anotherpassword"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Username already registered"}


def test_update_user_success(test_user: User, authenticated_client: TestClient, db_session: Session):
    # Update the user's first name and last name
    response = authenticated_client.put("/api/v1/users/", json={"name": "Updated", "last_name": "User"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated"
    assert data["last_name"] == "User"


def test_update_username_is_not_allowed(test_user: User, authenticated_client: TestClient, db_session: Session):
    response = authenticated_client.put("/api/v1/users/", json={"username": "newusername"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == test_user.username  # Username should remain unchanged


def test_update_user_password_success(test_user: User, authenticated_client: TestClient, db_session: Session):
    # Update the user's password
            # Update the user's password
    response = authenticated_client.put(
        "/api/v1/users/me/password/", json={"old_password": TEST_USER_RAW_PASS, "new_password": "newpassword456"}
    )
    assert response.status_code == status.HTTP_200_OK

    # Verify that the password was updated successfully
    updated_user = db_session.query(User).filter(User.id == test_user.id).first()
    assert updated_user is not None
    assert verify_password("newpassword456", updated_user.hashed_password)  # Check the new password
    assert not verify_password(TEST_USER_RAW_PASS, updated_user.hashed_password)  # Old password should no longer
