import asyncio
import sys
from fastapi.testclient import TestClient

try:
    from main import app
    print("✓ Main application imported successfully")
except Exception as e:
    print(f"✗ Error importing main app: {e}")
    sys.exit(1)

try:
    from app.database.mongodb import connect_to_mongo
    print("✓ MongoDB module imported successfully")
except Exception as e:
    print(f"✗ Error importing MongoDB module: {e}")

try:
    from app.config import settings
    print("✓ Config settings imported successfully")
    print(f"  - Database: {settings.DATABASE_NAME}")
    print(f"  - MongoDB URL: {settings.MONGODB_URL[:20]}...")  # Show first 20 chars for security
except Exception as e:
    print(f"✗ Error importing config: {e}")

# Test the application
client = TestClient(app)

print("\nTesting endpoints:")
endpoints_to_test = [
    ("GET", "/"),
    ("GET", "/docs"),
    ("GET", "/openapi.json"),
    ("POST", "/user/register"),
    ("POST", "/user/login"),
    ("GET", "/parkings/"),
    ("GET", "/bookings/"),
    ("GET", "/notifications/")
]

for method, endpoint in endpoints_to_test:
    try:
        if method == "GET":
            response = client.get(endpoint)
        elif method == "POST":
            response = client.post(endpoint, json={})
        
        print(f"✓ {method} {endpoint}: {response.status_code}")
    except Exception as e:
        print(f"✗ {method} {endpoint}: Error - {e}")

print("\nTesting database connection:")
try:
    async def test_db():
        await connect_to_mongo()
        print("✓ MongoDB connection successful")
    
    asyncio.run(test_db())
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")

print("\nApplication test completed!")
