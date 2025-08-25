import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import uuid

async def seed_database():
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    # Clear existing data
    await db["parking_lots"].delete_many({})
    await db["slots"].delete_many({})
    await db["users"].delete_many({})
    await db["bookings"].delete_many({})
    await db["notifications"].delete_many({})
    
    # Create parking lots
    parking_lots = [
        {
            "lot_id": "LOT-001",
            "lot_name": "Central Mall Parking",
            "location": "Downtown"
        },
        {
            "lot_id": "LOT-002", 
            "lot_name": "Tech Park Parking",
            "location": "IT Hub"
        },
        {
            "lot_id": "LOT-003",
            "lot_name": "University Parking",
            "location": "Campus Area"
        },
        {
            "lot_id": "LOT-004",
            "lot_name": "Shopping Center Parking",
            "location": "Commercial District"
        },
        {
            "lot_id": "LOT-005",
            "lot_name": "Hospital Parking",
            "location": "Medical Area"
        }
    ]
    
    await db["parking_lots"].insert_many(parking_lots)
    
    # Create slots for each parking lot
    slots = []
    for lot in parking_lots:
        for i in range(1, 7):  # 6 slots per lot
            slot_type = "car" if i % 2 == 0 else "bike"
            slots.append({
                "slot_id": f"S{i}",
                "parking_id": lot["lot_id"],
                "vehicle_type": slot_type,
                "status": "available",
                "current_booking_id": None
            })
    
    await db["slots"].insert_many(slots)
    
    # Create a test user
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    test_user = {
        "_id": str(uuid.uuid4()),
        "username": "testuser",
        "email": "test@example.com",
        "phone": "9876543210",
        "hashed_password": pwd_context.hash("password123"),
        "role": "user",
        "is_active": True,
        "created_at": "2025-08-01T10:15:30Z",
        "last_login": None
    }
    
    await db["users"].insert_one(test_user)
    
    print("Database seeded successfully!")
    print(f"Test user: test@example.com / password123")
    print(f"Created {len(parking_lots)} parking lots with {len(slots)} total slots")

if __name__ == "__main__":
    asyncio.run(seed_database())
