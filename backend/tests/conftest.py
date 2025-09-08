from typing import Final
import pytest
from app.db.base import Base, get_db
from app.main import app
from app.users.models import User
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


TEST_USER_RAW_PASS:Final[str]="sircrapsalot"

@pytest.fixture
def db_session():
    """Create a new database session for each test function.
    Rollback any changes after the test is done.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: TestingSessionLocal):
    """Create a test client that uses the override_get_db fixture to use the
    in-memory database.
    """

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture
def test_user(db_session: TestingSessionLocal):
    from app.core.security import get_password_hash

    user = User(
        username="sirloin",
        email="sir.loin@example.com",
        hashed_password=get_password_hash(TEST_USER_RAW_PASS),
        name="Sir Loin",
        last_name="of Testington",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def payment_method_in_db(db_session: TestingSessionLocal):
    from app.payments.models import PaymentMethod
    payment_method = PaymentMethod(name="Cash")
    db_session.add(payment_method)
    db_session.commit()
    db_session.refresh(payment_method)
    return payment_method


@pytest.fixture
def authenticated_client(client: TestClient, test_user: User):
    from app.core.security import create_access_token

    access_token = create_access_token(data={"sub": test_user.username})
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}",
    }
    return client
