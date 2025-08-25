
import asyncio

from fastapi import FastAPI
from app.config.db import get_db
from app.config.settings import settings
from app.utils.auth import hash_password

app = FastAPI()

LOTS = [
    {"lot_name": "Central Mall Parking", "location": "Downtown"},
    {"lot_name": "Tech Park Parking", "location": "IT Hub"},
    {"lot_name": "Railway Station Parking", "location": "Transit Zone"},
    {"lot_name": "Stadium Parking", "location": "Sports Complex"},
    {"lot_name": "Airport Parking", "location": "Airport Road"},
]

VEH_TYPES = ["car", "bike", "car", "bike", "car", "bike"]  # 6 slots per lot

async def run():
    db = get_db()

    # Clean existing
    for coll in ["users", "parking_lots", "slots", "bookings", "notifications"]:
        await db[coll].delete_many({})

    # Create a sample user
    await db["users"].insert_one({
        "username": "surendra",
        "email": "surendra@example.com",
        "phone": "9876543210",
        "password_hash": hash_password("mypassword123"),
        "role": "user",
        "created_at": None,
        "is_active": True,
        "reset_token": None,
        "reset_token_created_at": None,
        "last_login": None,
    })

    # Seed lots and slots
    for lot in LOTS:
        res = await db["parking_lots"].insert_one(lot)
        lot_id = str(res.inserted_id)
        slots = []
        for i in range(6):
            slots.append({
                "parking_id": lot_id,
                "slot_id": f"S{i+1:02d}",
                "vehicle_type": VEH_TYPES[i],
                "status": "available",
            })
        await db["slots"].insert_many(slots)

    print("✅ Seed completed: 5 lots × 6 slots + 1 user")

if __name__ == "__main__":
    asyncio.run(run())
