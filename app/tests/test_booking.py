import uuid
from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_booking_flow():
    username = f"testuser_{uuid.uuid4()}"

    response = client.post("/auth/register", json={"username": username, "password": "testpass"})
    assert response.status_code == 200

    response = client.post("/auth/login", data={"username": username, "password": "testpass"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/rooms/", json={
        "name": f"Test Room {uuid.uuid4()}",
    })
    assert response.status_code in [200, 201]
    room_id = response.json()["id"]

    future_date = (date.today() + timedelta(days=30)).isoformat()

    response = client.post("/bookings", json={
        "room_id": room_id,
        "date": future_date,
        "start_time": "10:00:00",
        "end_time": "11:00:00"
    }, headers=headers)
    assert response.status_code in [200, 201]
    booking_id = response.json()["id"]

    response = client.get("/bookings", headers=headers)
    assert response.status_code == 200

    response = client.delete(f"/bookings/{booking_id}", headers=headers)
    assert response.status_code == 200