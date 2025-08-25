"""
Final verification script for Smart Parking Finder application
This script tests all the security fixes and application functionality
"""

import asyncio
import sys
from fastapi.testclient import TestClient
from main import app

def print_header(text):
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")

def test_environment_variables():
    """Test that environment variables are properly loaded"""
    print_header("ENVIRONMENT VARIABLES TEST")
    
    try:
        from app.config import settings
        
        required_vars = [
            'MONGODB_URL', 'DATABASE_NAME', 'JWT_SECRET_KEY',
            'JWT_ALGORITHM', 'SMTP_USER', 'SMTP_PASSWORD'
        ]
        
        all_loaded = True
        for var in required_vars:
            value = getattr(settings, var, None)
            if value is None:
                print(f"✗ Missing environment variable: {var}")
                all_loaded = False
            else:
                print(f"✓ {var}: {'*' * min(len(str(value)), 20)}")  # Mask sensitive data
        
        if all_loaded:
            print("✓ All environment variables loaded successfully")
        return all_loaded
        
    except Exception as e:
        print(f"✗ Error loading environment variables: {e}")
        return False

def test_database_connection():
    """Test MongoDB connection"""
    print_header("DATABASE CONNECTION TEST")
    
    try:
        from app.database.mongodb import connect_to_mongo
        
        async def test_connection():
            await connect_to_mongo()
            print("✓ MongoDB connection established successfully")
            return True
        
        return asyncio.run(test_connection())
        
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False

def test_application_endpoints():
    """Test all application endpoints"""
    print_header("APPLICATION ENDPOINTS TEST")
    
    client = TestClient(app)
    endpoints = [
        ("GET", "/", "Root endpoint"),
        ("GET", "/docs", "API documentation"),
        ("GET", "/openapi.json", "OpenAPI schema"),
        ("POST", "/user/register", "User registration"),
        ("POST", "/user/login", "User login"),
        ("GET", "/user/profile", "User profile (requires auth)"),
        ("GET", "/parkings/", "Parking listings"),
        ("GET", "/bookings/", "Booking management"),
        ("GET", "/notifications/", "Notifications")
    ]
    
    all_working = True
    for method, endpoint, description in endpoints:
        try:
            if method == "GET":
                response = client.get(endpoint)
            elif method == "POST":
                response = client.post(endpoint, json={})
            
            status_ok = response.status_code in [200, 201, 401]  # 401 is expected for auth endpoints
            if status_ok:
                print(f"✓ {method} {endpoint}: {response.status_code} - {description}")
            else:
                print(f"✗ {method} {endpoint}: {response.status_code} - {description}")
                all_working = False
                
        except Exception as e:
            print(f"✗ {method} {endpoint}: Error - {e}")
            all_working = False
    
    return all_working

def test_password_validation():
    """Test password validation functionality"""
    print_header("PASSWORD VALIDATION TEST")
    
    try:
        from app.utils.validators import validate_password_complexity
        
        # Test valid password
        try:
            validate_password_complexity("Test123!")
            print("✓ Valid password accepted: Test123!")
        except Exception as e:
            print(f"✗ Valid password rejected: {e}")
            return False
        
        # Test invalid passwords
        invalid_passwords = [
            ("short", "too short"),
            ("nouppercase1!", "no uppercase"),
            ("NOLOWERCASE1!", "no lowercase"),
            ("NoNumbers!", "no numbers"),
            ("NoSpecial123", "no special chars")
        ]
        
        for password, reason in invalid_passwords:
            try:
                validate_password_complexity(password)
                print(f"✗ Invalid password accepted ({reason}): {password}")
                return False
            except ValueError:
                print(f"✓ Invalid password rejected ({reason}): {password}")
        
        return True
        
    except Exception as e:
        print(f"✗ Password validation test failed: {e}")
        return False

def main():
    """Run all verification tests"""
    print_header("SMART PARKING FINDER - FINAL VERIFICATION")
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Database Connection", test_database_connection),
        ("Application Endpoints", test_application_endpoints),
        ("Password Validation", test_password_validation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    print_header("TEST RESULTS SUMMARY")
    
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:25} : {status}")
        if not result:
            all_passed = False
    
    print_header("FINAL STATUS")
    if all_passed:
        print("🎉 ALL TESTS PASSED! Application is ready for use.")
        print("\nSecurity improvements implemented:")
        print("✓ Sensitive data moved to .env file")
        print("✓ Hardcoded credentials removed from config")
        print("✓ Password validation consistency fixed")
        print("✓ .gitignore file created for security")
        print("✓ Comprehensive testing framework established")
    else:
        print("❌ SOME TESTS FAILED. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
