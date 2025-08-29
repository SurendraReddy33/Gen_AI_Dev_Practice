import asyncio
from app.db.mongo_db import db

async def seed_initial_data():
    lots_collection = db["parking_lots"]

    existing_lots = await lots_collection.count_documents({})
    if existing_lots > 0:
        print("✅ Initial parking lots already exist, skipping seeding...")
        return

    vehicle_types = ["car", "bike"]  # alternate slot types

    lots = []
    for lot_id in range(1, 6):  # 5 lots
        slots = []
        for slot_id in range(1, 7):  # 6 slots per lot
            slots.append({
                "slot_id": f"{lot_id}-{slot_id}",
                "vehicle_type": vehicle_types[slot_id % 2],
                "status": "available",   # initially all available
            })

        lots.append({
            "lot_id": lot_id,
            "lot_name": f"Parking Lot {lot_id}",
            "location": f"Area {lot_id}",
            "total_slots": slots,
            "available_slots": len(slots),  # all available initially
            "booked_slots": 0
        })

    await lots_collection.insert_many(lots)
    print("🚀 Initial parking lots with nested slots seeded successfully!")
