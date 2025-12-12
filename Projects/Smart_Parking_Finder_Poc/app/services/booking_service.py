from fastapi import HTTPException
from app.db.mongo_db import db, parkings_collection, bookings_collection
from app.models.booking_models import CreateBookingRequest
from app. utils.logger import get_logger
from app.core.security import verify_jwt
from datetime import datetime
import uuid

logger = get_logger(__name__)

async def create_booking(data: CreateBookingRequest, user: dict):
    lot_id = data.lot_id
    slot_id = data.slot_id
    vehicle_type = data.vehicle_type

    # ✅ Get email from JWT user (not from request body)
    user_email = user.get("email")

    if not user_email:
        raise HTTPException(status_code=400, detail="Invalid user: email missing from token")

    # 1️⃣ Find the parking lot
    lot = await db["parking_lots"].find_one({"lot_id": int(lot_id)})
    if not lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")

    # 2️⃣ Find the slot in nested total_slots
    slot = next((s for s in lot["total_slots"] if s["slot_id"] == slot_id), None)
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    if slot["vehicle_type"] != vehicle_type:
        raise HTTPException(status_code=400, detail="Invalid vehicle type for this slot")

    if slot["status"] != "available":
        raise HTTPException(status_code=409, detail="Slot already booked")

    # 3️⃣ Generate booking
    booking_id = "B" + uuid.uuid4().hex[:8].upper()
    now = datetime.utcnow()

    # Store booking in "bookings" collection
    await db["bookings"].insert_one({
        "booking_id": booking_id,
        "user_email": user_email,  # ✅ taken from JWT
        "lot_id": lot["lot_id"],
        "slot_id": slot_id,
        "vehicle_type": vehicle_type,
        "status": "active",
        "created_at": now
    })

    # 4️⃣ Update slot status
    for s in lot["total_slots"]:
        if s["slot_id"] == slot_id:
            s["status"] = "booked"

    # 5️⃣ Update lot counts
    available_count = sum(1 for s in lot["total_slots"] if s["status"] == "available")
    booked_count = len(lot["total_slots"]) - available_count

    await db["parking_lots"].update_one(
        {"lot_id": lot["lot_id"]},
        {"$set": {
            "total_slots": lot["total_slots"],
            "available_slots": available_count,
            "booked_slots": booked_count
        }}
    )

    logger.info(f"Booking created: {booking_id} for slot {slot_id} in lot {lot_id} by {user_email}")

    return {
        "message": "Booking successful. Slot reserved.",
        "booking_id": booking_id,
        "lot_id": lot["lot_id"],
        "slot_id": slot_id,
        "vehicle_type": vehicle_type,
        "user_email": user_email
    }

    
async def list_bookings(user_email: str | None = None):
    query = {}
    if user_email:
        query["user_email"] = user_email

    bookings = await db["bookings"].find(query).to_list(None)
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found")

    results = []
    for b in bookings:
        results.append({
            "booking_id": b["booking_id"],
            "user_email": b["user_email"],
            "lot_id": b["lot_id"],
            "slot_id": b["slot_id"],
            "vehicle_type": b["vehicle_type"],
            "status": b["status"],
            "created_at": b["created_at"]
        })

    return results


async def get_booking_by_id(booking_id: str):
    booking = await db["bookings"].find_one({"booking_id": booking_id})
    
    if not booking:
        logger.warning(f"Booking not found: {booking_id}")
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Convert lot_id to string for response consistency
    booking["lot_id"] = str(booking["lot_id"])
    
    return booking

async def update_booking(booking_id: str, new_slot_id: str = None, new_vehicle_type: str = None):
    # 1️⃣ Find the booking
    booking = await db["bookings"].find_one({"booking_id": booking_id})
    if not booking:
        logger.warning(f"Booking not found: {booking_id}")
        raise HTTPException(status_code=404, detail="Booking not found")

    # 2️⃣ Find the lot
    lot = await db["parking_lots"].find_one({"lot_id": int(booking["lot_id"])})
    if not lot:
        logger.warning(f"Parking lot not found for booking {booking_id}")
        raise HTTPException(status_code=404, detail="Parking lot not found")

    updated_fields = {}

    # 3️⃣ Update slot if requested
    if new_slot_id:
        slot = next((s for s in lot["total_slots"] if s["slot_id"] == new_slot_id), None)
        if not slot:
            raise HTTPException(status_code=404, detail="Slot not found")
        if slot["status"] != "available":
            raise HTTPException(status_code=409, detail="Slot already booked")
        # Mark previous slot as available
        for s in lot["total_slots"]:
            if s["slot_id"] == booking["slot_id"]:
                s["status"] = "available"
        # Mark new slot as booked
        slot["status"] = "booked"
        updated_fields["slot_id"] = new_slot_id

    # 4️⃣ Update vehicle type if requested
    if new_vehicle_type:
        slot_to_check = next((s for s in lot["total_slots"] if s["slot_id"] == updated_fields.get("slot_id", booking["slot_id"])), None)
        if slot_to_check and slot_to_check["vehicle_type"] != new_vehicle_type:
            raise HTTPException(status_code=400, detail="Vehicle type does not match the slot")
        updated_fields["vehicle_type"] = new_vehicle_type

    if not updated_fields:
        raise HTTPException(status_code=400, detail="No valid fields provided to update")

    # 5️⃣ Update booking in DB
    await db["bookings"].update_one(
        {"booking_id": booking_id},
        {"$set": updated_fields}
    )

    # 6️⃣ Update parking lot counts
    available_count = sum(1 for s in lot["total_slots"] if s["status"] == "available")
    booked_count = len(lot["total_slots"]) - available_count
    await db["parking_lots"].update_one(
        {"lot_id": lot["lot_id"]},
        {"$set": {"total_slots": lot["total_slots"], "available_slots": available_count, "booked_slots": booked_count}}
    )

    logger.info(f"Booking {booking_id} updated successfully")

    return {"message": "Booking updated successfully", "booking_id": booking_id, **updated_fields}


async def release_booking(booking_id: str):
    # 1️⃣ Find the booking
    booking = await db["bookings"].find_one({"booking_id": booking_id})
    if not booking:
        logger.warning(f"Booking not found: {booking_id}")
        raise HTTPException(status_code=404, detail="Booking not found")

    # 2️⃣ Find the parking lot
    lot = await db["parking_lots"].find_one({"lot_id": int(booking["lot_id"])})
    if not lot:
        logger.warning(f"Parking lot not found for booking {booking_id}")
        raise HTTPException(status_code=404, detail="Parking lot not found")

    # 3️⃣ Mark the slot as available
    slot = next((s for s in lot["total_slots"] if s["slot_id"] == booking["slot_id"]), None)
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found in lot")
    slot["status"] = "available"

    # 4️⃣ Delete the booking from bookings collection
    await db["bookings"].delete_one({"booking_id": booking_id})

    # 5️⃣ Update parking lot slot counts
    available_count = sum(1 for s in lot["total_slots"] if s["status"] == "available")
    booked_count = len(lot["total_slots"]) - available_count

    await db["parking_lots"].update_one(
        {"lot_id": lot["lot_id"]},
        {"$set": {
            "total_slots": lot["total_slots"],
            "available_slots": available_count,
            "booked_slots": booked_count
        }}
    )

    logger.info(f"Booking {booking_id} released and deleted successfully")

    return {
        "message": "Booking released and deleted successfully",
        "booking_id": booking_id,
        "lot_id": booking["lot_id"],
        "slot_id": booking["slot_id"],
        "status": "released"
    }

