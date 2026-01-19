from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data
    assert "participants" in data["Basketball"]

def test_signup_success():
    # Sign up a new student
    response = client.post("/activities/Basketball/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@example.com for Basketball" in data["message"]

    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Basketball"]["participants"]

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Tennis Club/signup?email=duplicate@example.com")
    # Second signup should fail
    response = client.post("/activities/Tennis Club/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up" in data["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # First sign up
    client.post("/activities/Art Studio/signup?email=unregister@example.com")
    # Then unregister
    response = client.delete("/activities/Art Studio/unregister?email=unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered unregister@example.com from Art Studio" in data["message"]

    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@example.com" not in data["Art Studio"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Debate Team/unregister?email=notsigned@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "Student not signed up" in data["detail"]

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent/unregister?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 307  # Temporary redirect
    assert "/static/index.html" in response.headers["location"]