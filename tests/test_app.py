import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities

def test_get_activities():
    # Arrange
    # (TestClient already arranged)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Club" in data

# Test POST /activities/{activity_name}/signup (success)

def test_signup_for_activity_success():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Confirm participant added
    get_response = client.get("/activities")
    assert email in get_response.json()[activity]["participants"]

# Test POST /activities/{activity_name}/signup (duplicate)

def test_signup_for_activity_duplicate():
    # Arrange
    activity = "Basketball Club"
    email = "alex@mergington.edu"  # already signed up
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"

# Test POST /activities/{activity_name}/signup (activity not found)

def test_signup_for_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
