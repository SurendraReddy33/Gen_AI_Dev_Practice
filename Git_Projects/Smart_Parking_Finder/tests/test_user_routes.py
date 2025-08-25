import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Smart Parking Finder API"}

def test_user_registration_endpoint():
    """Test user registration endpoint exists."""
    response = client.post("/user/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "phone": "1234567890",
        "password": "Test123!"
    })
    # This should either succeed (201) or fail with conflict (409) if user exists
    assert response.status_code in [201, 409]

def test_user_login_endpoint():
    """Test user login endpoint exists."""
    response = client.post("/user/login", data={
        "username": "testuser",
        "password": "Test123!"
    })
    # This should either succeed (200) or fail with unauthorized (401)
    assert response.status_code in [200, 401]

def test_parking_endpoints():
    """Test parking endpoints exist."""
    response = client.get("/parkings/")
    assert response.status_code in [200, 401]  # 401 if requires auth

def test_booking_endpoints():
    """Test booking endpoints exist."""
    response = client.get("/bookings/")
    assert response.status_code in [200, 401]  # 401 if requires auth

if __name__ == "__main__":
    pytest.main([__file__])
