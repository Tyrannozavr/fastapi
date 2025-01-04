from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user():
    response = client.post("/users/",
                           json={"username": "testuser", "email": "test@example.com", "full_name": "Test User"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

test_create_user()