from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_user_success(client: TestClient, db_session: Session):
    """
    Test creating a user successfully.
    """
    response = client.post(
        "/api/v1/users/",
        json={"username": "testuser", "password": "testpassword123", "default_timezone": "UTC"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "hashed_password" not in data

def test_create_user_duplicate_username(client: TestClient, db_session: Session):
    """
    Test that creating a user with a duplicate username fails.
    """
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
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}
