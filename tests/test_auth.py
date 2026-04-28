import pytest
from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    user_data = {
        "email": "newuser@example.com",
        "password": "password123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"msg": "User created"}

def test_register_duplicate_user(client: TestClient):
    user_data = {
        "email": "duplicate@example.com",
        "password": "password123"
    }
    # First registration
    client.post("/auth/register", json=user_data)

    # Second registration should fail
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert "User already exists" in response.json()["detail"]

def test_login_success(client: TestClient):
    user_data = {
        "email": "loginuser@example.com",
        "password": "password123"
    }
    # Register first
    client.post("/auth/register", json=user_data)

    # Login
    response = client.post("/auth/login", data={
        "username": user_data["email"],
        "password": user_data["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient):
    response = client.post("/auth/login", data={
        "username": "nonexistent@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]

def test_login_wrong_password(client: TestClient):
    user_data = {
        "email": "wrongpass@example.com",
        "password": "correctpass"
    }
    # Register first
    client.post("/auth/register", json=user_data)

    # Login with wrong password
    response = client.post("/auth/login", data={
        "username": user_data["email"],
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]