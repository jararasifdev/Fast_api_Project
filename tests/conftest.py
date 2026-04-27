import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
import os
from dotenv import load_dotenv
import os


load_dotenv()

TEST_DATABASE_URL = os.getenv("DATABASE_URL")  # or TEST_DATABASE_URL

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with a test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "testpass123"
    }

@pytest.fixture
def auth_headers(client, test_user_data):
    """Register a user and return auth headers."""
    # Register user
    client.post("/auth/register", json=test_user_data)

    # Login and get token
    response = client.post("/auth/login", data={
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}