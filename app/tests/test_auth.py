import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_auth_flow():
    username = f"testuser_{uuid.uuid4()}"

    #register
    response = client.post("/auth/register", json={"username": username, "password": "testpass"})
    assert response.status_code == 200

    #login
    response = client.post("/auth/login", data={"username": username, "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    token = response.json()["access_token"]

    #check me
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
