from app.db.mongo_db import db, parkings_collection, slots_collection, login_sessions_collection
from fastapi import HTTPException, Header, Query
from bson import ObjectId
from app.models.parking_models import ParkingLotResponse
from app.core.security import verify_jwt
from app.core.dependencies import validate_token
from fastapi import HTTPException
from app.db.mongo_db import db
from app.utils.logger import get_logger


logger = get_logger(__name__)

async def list_parkings_service(token: str, vehicle_type: str = None):
    # Validate token & session
    payload = await validate_token(token)
    user_email = payload.get("email")

    # Fetch parking lots    
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
            "lot_id": int(lot.get("lot_id")),
            "lot_name": lot.get("lot_name"),
            "location": lot.get("location"),
            "total_slots": total,
            "available_slots": avail,
            "booked_slots": booked,
        })

    return results



async def parking_details(lot_id: int) -> dict:
    parkings_collection = db["parking_lots"]

    lot = await parkings_collection.find_one({"lot_id": lot_id})
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
async def available_slots_by_vehicle_type(vehicle_type: str | None = None) -> dict:
    pipeline = [
        {"$unwind": "$total_slots"},  # flatten slots array
        {
            "$match": {
                "total_slots.status": "available"
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

    # if vehicle_type filter provided, add it dynamically
    if vehicle_type:
        pipeline[1]["$match"]["total_slots.vehicle_type"] = vehicle_type

    slots = await parkings_collection.aggregate(pipeline).to_list(None)

    return {
        "available_slots": slots,
        "count": len(slots)
    }

