import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Smart Parking Finder API"}

def test_user_registration():
    """Test user registration with valid data."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "phone": "1234567890",
        "password": "Test123!"
    }
    response = client.post("/user/register", json=user_data)
    assert response.status_code in [201, 409]  # 201 created or 409 if user exists

def test_user_registration_invalid_password():
    """Test user registration with invalid password."""
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "phone": "0987654321",
        "password": "weak"  # Too short
    }
    response = client.post("/user/register", json=user_data)
    assert response.status_code == 422  # Validation error

def test_user_login():
    """Test user login functionality."""
    response = client.post("/user/login", data={
        "username": "testuser",
        "password": "Test123!"
    })
    assert response.status_code in [200, 401]  # 200 success or 401 unauthorized

def test_user_login_invalid_credentials():
    """Test user login with invalid credentials."""
    response = client.post("/user/login", data={
        "username": "nonexistent",
        "password": "wrongpassword"
    })
    assert response.status_code == 401  # Unauthorized

def test_parking_endpoints_accessible():
    """Test parking endpoints are accessible."""
    response = client.get("/parkings/")
    assert response.status_code in [200, 401]  # 200 if public, 401 if requires auth

def test_booking_endpoints_accessible():
    """Test booking endpoints are accessible."""
    response = client.get("/bookings/")
    assert response.status_code in [200, 401]  # 200 if public, 401 if requires auth

def test_notification_endpoints_accessible():
    """Test notification endpoints are accessible."""
    response = client.get("/notifications/")
    assert response.status_code in [200, 401]  # 200 if public, 401 if requires auth

def test_user_profile_requires_auth():
    """Test user profile endpoint requires authentication."""
    response = client.get("/user/profile")
    assert response.status_code == 401  # Unauthorized

def test_password_change_requires_auth():
    """Test password change endpoint requires authentication."""
    response = client.put("/user/password/change", json={
        "old_password": "oldpass",
        "new_password": "newpass"
    })
    assert response.status_code == 401  # Unauthorized

def test_api_documentation_available():
    """Test that API documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200  # Swagger UI should be available

def test_openapi_schema_available():
    """Test that OpenAPI schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200  # OpenAPI schema should be available
    assert "openapi" in response.json()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
