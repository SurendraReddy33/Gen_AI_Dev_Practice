
from fastapi import HTTPException
from bson import ObjectId
from app.config.db import get_db
from app.models import PARKINGS_COLL, SLOTS_COLL

def _oid(obj): return ObjectId(obj) if ObjectId.is_valid(obj) else obj

async def list_parkings(vehicle_type: str | None = None) -> list[dict]:
    db = get_db()
    lots = await db[PARKINGS_COLL].find({}).to_list(None)
    results = []
    for lot in lots:
        q = {"parking_id": str(lot["_id"])}
        if vehicle_type:
            q["vehicle_type"] = vehicle_type
        slots = await db[SLOTS_COLL].find(q).to_list(None)
        total = len(slots)
        avail = len([s for s in slots if s.get("status") == "available"])
        results.append({
            "lot_id": str(lot["_id"]),
            "lot_name": lot.get("lot_name"),
            "location": lot.get("location"),
            "total_slots": total,
            "available_slots": avail,
            "booked_slots": total - avail,
        })
    return results

async def parking_details(parking_id: str) -> dict:
    db = get_db()
    lot = await db[PARKINGS_COLL].find_one({"_id": _oid(parking_id)})
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")

    slots = await db[SLOTS_COLL].find({"parking_id": str(lot["_id"])}).to_list(None)
    total = len(slots)
    avail = len([s for s in slots if s.get("status") == "available"])
    return {
        "parking_id": str(lot["_id"]),
        "lot_name": lot.get("lot_name"),
        "total_slots": total,
        "available_slots": avail,
        "booked_slots": total - avail,
        "slots": [{
            "slot_id": s["slot_id"],
            "type": s.get("vehicle_type"),
            "status": s.get("status", "available")
        } for s in slots]
    }

async def parking_slots(parking_id: str) -> dict:
    db = get_db()
    lot = await db[PARKINGS_COLL].find_one({"_id": _oid(parking_id)})
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")

    slots = await db[SLOTS_COLL].find({"parking_id": str(lot["_id"])}).to_list(None)
    return {
        "parking_id": str(lot["_id"]),
        "lot_name": lot.get("lot_name"),
        "total_slots": len(slots),
        "slots": [{
            "slot_id": s["slot_id"],
            "vehicle_type": s.get("vehicle_type"),
            "status": s.get("status", "available"),
            "current_booking_id": s.get("current_booking_id")
        } for s in slots]
    }

async def available_slots(parking_id: str, vehicle_type: str | None) -> dict:
    db = get_db()
    lot = await db[PARKINGS_COLL].find_one({"_id": _oid(parking_id)})
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")

    q = {"parking_id": str(lot["_id"]), "status": "available"}
    if vehicle_type:
        q["vehicle_type"] = vehicle_type
    slots = await db[SLOTS_COLL].find(q).to_list(None)
    return {
        "parking_id": str(lot["_id"]),
        "available_slots": [{
            "slot_id": s["slot_id"],
            "vehicle_type": s.get("vehicle_type"),
            "status": s.get("status", "available"),
        } for s in slots],
        "count": len(slots)
    }
