
from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId
import uuid

from app.config.db import get_db
from app.models import PARKINGS_COLL, SLOTS_COLL, BOOKINGS_COLL, NOTIFS_COLL

def _oid(obj): return ObjectId(obj) if ObjectId.is_valid(obj) else obj

async def create_booking(user_id: str, parking_id: str, slot_id: str, vehicle_type: str) -> dict:
    db = get_db()
    lot = await db[PARKINGS_COLL].find_one({"_id": _oid(parking_id)})
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")

    slot = await db[SLOTS_COLL].find_one({"parking_id": str(lot["_id"]), "slot_id": slot_id})
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    if slot.get("vehicle_type") != vehicle_type:
        raise HTTPException(status_code=400, detail="Invalid vehicle type for this slot")
    if slot.get("status") != "available":
        raise HTTPException(status_code=409, detail="Slot already booked")

    booking_id = "B" + uuid.uuid4().hex[:8].upper()
    now = datetime.utcnow()
    await db[BOOKINGS_COLL].insert_one({
        "booking_id": booking_id,
        "user_id": user_id,
        "parking_id": str(lot["_id"]),
        "slot_id": slot_id,
        "vehicle_type": vehicle_type,
        "status": "active",
        "created_at": now
    })
    await db[SLOTS_COLL].update_one({"_id": slot["_id"]}, {"$set": {"status": "booked", "current_booking_id": booking_id}})
    await db[NOTIFS_COLL].insert_one({
        "user_id": user_id,
        "type": "booking",
        "message": f"Your booking {booking_id} is confirmed for slot {slot_id} at parking {lot.get('lot_name')}",
        "status": "unread",
        "created_at": now
    })
    return {
        "booking_id": booking_id,
        "user_id": user_id,
        "parking_id": str(lot["_id"]),
        "slot_id": slot_id,
        "vehicle_type": vehicle_type,
        "status": "active",
        "created_at": now,
        "message": "Booking successful. Slot reserved."
    }

async def list_bookings(user_id: str) -> list[dict]:
    db = get_db()
    docs = await db[BOOKINGS_COLL].find({"user_id": user_id}).sort("created_at", -1).to_list(None)
    return docs

async def get_booking(user_id: str, booking_id: str) -> dict:
    db = get_db()
    doc = await db[BOOKINGS_COLL].find_one({"user_id": user_id, "booking_id": booking_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Booking not found")
    return doc

async def update_booking(user_id: str, booking_id: str, slot_id: str | None, vehicle_type: str | None) -> dict:
    db = get_db()
    bk = await db[BOOKINGS_COLL].find_one({"user_id": user_id, "booking_id": booking_id})
    if not bk:
        raise HTTPException(status_code=404, detail="Booking not found")

    lot_id = bk["parking_id"]
    updates = {}

    if slot_id:
        # check target slot availability in same lot
        slot = await db[SLOTS_COLL].find_one({"parking_id": lot_id, "slot_id": slot_id})
        if not slot:
            raise HTTPException(status_code=404, detail="Slot not found")
        if slot.get("status") != "available":
            raise HTTPException(status_code=400, detail="Requested slot is already booked")
        # free old slot
        await db[SLOTS_COLL].update_one({"parking_id": lot_id, "slot_id": bk["slot_id"]},
                                        {"$set": {"status": "available"}, "$unset": {"current_booking_id": ""}})
        # assign new
        await db[SLOTS_COLL].update_one({"_id": slot["_id"]},
                                        {"$set": {"status": "booked", "current_booking_id": booking_id}})
        updates["slot_id"] = slot_id

    if vehicle_type:
        # verify vehicle type matches new/old slot
        target_slot_id = updates.get("slot_id", bk["slot_id"])
        target_slot = await db[SLOTS_COLL].find_one({"parking_id": lot_id, "slot_id": target_slot_id})
        if target_slot and target_slot.get("vehicle_type") != vehicle_type:
            raise HTTPException(status_code=400, detail="Vehicle type does not match the slot type")
        updates["vehicle_type"] = vehicle_type

    updates["created_at"] = datetime.utcnow()
    await db[BOOKINGS_COLL].update_one({"_id": bk["_id"]}, {"$set": updates})

    bk = await db[BOOKINGS_COLL].find_one({"_id": bk["_id"]})
    return bk

async def delete_booking(user_id: str, booking_id: str) -> dict:
    db = get_db()
    bk = await db[BOOKINGS_COLL].find_one({"user_id": user_id, "booking_id": booking_id})
    if not bk:
        raise HTTPException(status_code=404, detail="Booking not found")

    # free slot
    await db[SLOTS_COLL].update_one({"parking_id": bk["parking_id"], "slot_id": bk["slot_id"]},
                                    {"$set": {"status": "available"}, "$unset": {"current_booking_id": ""}})
    await db[BOOKINGS_COLL].update_one({"_id": bk["_id"]}, {"$set": {"status": "cancelled", "cancelled_at": datetime.utcnow()}})
    await db[NOTIFS_COLL].insert_one({
        "user_id": user_id,
        "type": "cancellation",
        "message": f"Your booking {booking_id} has been cancelled.",
        "status": "unread",
        "created_at": datetime.utcnow()
    })
    bk = await db[BOOKINGS_COLL].find_one({"_id": bk["_id"]})
    return bk

async def release_booking(user_id: str, booking_id: str) -> dict:
    db = get_db()
    bk = await db[BOOKINGS_COLL].find_one({"user_id": user_id, "booking_id": booking_id})
    if not bk:
        raise HTTPException(status_code=404, detail="Booking not found")

    # free slot
    await db[SLOTS_COLL].update_one({"parking_id": bk["parking_id"], "slot_id": bk["slot_id"]},
                                    {"$set": {"status": "available"}, "$unset": {"current_booking_id": ""}})
    await db[BOOKINGS_COLL].update_one({"_id": bk["_id"]}, {"$set": {"status": "released", "released_at": datetime.utcnow()}})
    await db[NOTIFS_COLL].insert_one({
        "user_id": user_id,
        "type": "release",
        "message": f"You successfully released slot {bk['slot_id']} at parking {bk['parking_id']}.",
        "status": "unread",
        "created_at": datetime.utcnow()
    })
    bk = await db[BOOKINGS_COLL].find_one({"_id": bk["_id"]})
    return bk
