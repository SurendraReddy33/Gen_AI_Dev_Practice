from app.db.mongo_db import db, parkings_collection, slots_collection
from fastapi import HTTPException, Query
from bson import ObjectId

async def list_parkings(vehicle_type: str | None = None) -> list[dict]:
    lots = await db["parking_lots"].find({}).to_list(None)
    if not lots:
        raise HTTPException(status_code=404, detail="No parking lots found")

    results = []
    for lot in lots:
        slots = lot.get("total_slots", [])
        if vehicle_type:
            slots = [s for s in slots if s.get("vehicle_type") == vehicle_type]

        total = len(slots)
        avail = len([s for s in slots if s.get("status") == "available"])
        booked = total - avail

        results.append({
            "lot_id": str(lot.get("lot_id")),
            "lot_name": lot.get("lot_name"),
            "location": lot.get("location"),
            "total_slots": total,
            "available_slots": avail,
            "booked_slots": booked,
        })

    return results


async def parking_details(lot_id: int) -> dict:
    parkings_collection = db["parking_lots"]

    lot = await db["parking_lots"].find_one({"lot_id": lot_id})
    print(lot)
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")

    slots = lot.get("total_slots", [])
    total = len(slots)
    avail = len([s for s in slots if s.get("status") == "available"])
    booked = total - avail

    return {
        "lot_id": lot.get("lot_id"),
        "lot_name": lot.get("lot_name"),
        "location": lot.get("location"),
        "total_slots": total,
        "available_slots": avail,
        "booked_slots": booked,
        "slots": [
            {
                "slot_id": s["slot_id"],
                "vehicle_type": s.get("vehicle_type"),
                "status": s.get("status", "available")
            }
            for s in slots
        ]
    }


async def available_slots(vehicle_type: str | None = Query(default=None)) -> dict:
    # Build match stage for slot level
    match_stage = {"total_slots.status": "available"}
    if vehicle_type:
        match_stage["total_slots.vehicle_type"] = vehicle_type

    pipeline = [
        {"$unwind": "$total_slots"},
        {"$match": match_stage},
        {
            "$project": {
                "_id": 0,
                "lot_id": "$lot_id",
                "lot_name": "$lot_name",
                "slot_id": "$total_slots.slot_id",
                "vehicle_type": "$total_slots.vehicle_type",
                "status": "$total_slots.status"
            }
        }
    ]

    slots = await parkings_collection.aggregate(pipeline).to_list(None)

    return {
        "available_slots": slots,
        "count": len(slots)
    }

# ✅ Service function to get available slots by vehicle type
async def available_slots_by_vehicle_type(vehicle_type: str) -> dict:
    pipeline = [
        {"$unwind": "$total_slots"},  # flatten slots array
        {
            "$match": {
                "total_slots.status": "available",
                "total_slots.vehicle_type": vehicle_type
            }
        },
        {
            "$project": {
                "_id": 0,
                "lot_id": "$lot_id",
                "lot_name": "$lot_name",
                "slot_id": "$total_slots.slot_id",
                "vehicle_type": "$total_slots.vehicle_type",
                "status": "$total_slots.status"
            }
        }
    ]

    slots = await parkings_collection.aggregate(pipeline).to_list(None)

    return {
        "available_slots": slots,
        "count": len(slots)
    }

