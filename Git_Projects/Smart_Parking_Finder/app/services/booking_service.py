from datetime import datetime
from app.models.booking import BookingCreate, BookingUpdate, BookingStatus
from app.database.mongodb import get_database
from app.services.notification_service import NotificationService
import uuid

class BookingService:
    def __init__(self, db):
        self.db = db
        self.bookings_collection = db["bookings"]
        self.slots_collection = db["slots"]
        self.parking_collection = db["parking_lots"]
        self.notification_service = NotificationService(db)
    
    async def create_booking(self, user_id: str, booking_data: BookingCreate):
        # Check if parking exists
        parking = await self.parking_collection.find_one({"lot_id": booking_data.parking_id})
        if not parking:
            return None
        
        # Check if slot exists and is available
        slot = await self.slots_collection.find_one({
            "slot_id": booking_data.slot_id,
            "parking_id": booking_data.parking_id,
            "vehicle_type": booking_data.vehicle_type,
            "status": "available"
        })
        
        if not slot:
            return None
        
        # Create booking
        booking_id = f"BKG{str(uuid.uuid4())[:8].upper()}"
        booking_data = {
            "booking_id": booking_id,
            "user_id": user_id,
            "parking_id": booking_data.parking_id,
            "slot_id": booking_data.slot_id,
            "vehicle_type": booking_data.vehicle_type,
            "status": BookingStatus.ACTIVE,
            "created_at": datetime.utcnow(),
            "parking_name": parking["lot_name"]
        }
        
        # Start transaction
        session = await self.db.client.start_session()
        try:
            async with session.start_transaction():
                # Insert booking
                await self.bookings_collection.insert_one(booking_data, session=session)
                
                # Update slot status
                await self.slots_collection.update_one(
                    {"slot_id": booking_data["slot_id"], "parking_id": booking_data["parking_id"]},
                    {"$set": {
                        "status": "booked",
                        "current_booking_id": booking_id
                    }},
                    session=session
                )
                
                # Create notification
                await self.notification_service.create_notification(
                    user_id,
                    "booking",
                    f"Your booking {booking_id} is confirmed for slot {booking_data['slot_id']} at {parking['lot_name']}.",
                    session=session
                )
                
        except Exception:
            return None
        
        return booking_data
    
    async def get_user_bookings(self, user_id: str):
        return await self.bookings_collection.find({"user_id": user_id}).to_list(None)
    
    async def get_booking(self, booking_id: str, user_id: str):
        return await self.bookings_collection.find_one({
            "booking_id": booking_id,
            "user_id": user_id
        })
    
    async def update_booking(self, booking_id: str, user_id: str, update_data: BookingUpdate):
        booking = await self.get_booking(booking_id, user_id)
        if not booking:
            return None
        
        # Check if new slot is available
        if update_data.slot_id and update_data.slot_id != booking["slot_id"]:
            new_slot = await self.slots_collection.find_one({
                "slot_id": update_data.slot_id,
                "parking_id": booking["parking_id"],
                "status": "available"
            })
            
            if not new_slot:
                return None
        
        update_fields = {}
        if update_data.slot_id:
            update_fields["slot_id"] = update_data.slot_id
        if update_data.vehicle_type:
            update_fields["vehicle_type"] = update_data.vehicle_type
        
        result = await self.bookings_collection.update_one(
            {"booking_id": booking_id},
            {"$set": update_fields}
        )
        
        if result.modified_count > 0:
            return await self.get_booking(booking_id, user_id)
        return None
    
    async def cancel_booking(self, booking_id: str, user_id: str):
        booking = await self.get_booking(booking_id, user_id)
        if not booking:
            return False
        
        session = await self.db.client.start_session()
        try:
            async with session.start_transaction():
                # Update booking status
                await self.bookings_collection.update_one(
                    {"booking_id": booking_id},
                    {"$set": {"status": BookingStatus.CANCELLED}},
                    session=session
                )
                
                # Free the slot
                await self.slots_collection.update_one(
                    {"slot_id": booking["slot_id"], "parking_id": booking["parking_id"]},
                    {"$set": {
                        "status": "available",
                        "current_booking_id": None
                    }},
                    session=session
                )
                
                # Create notification
                await self.notification_service.create_notification(
                    user_id,
                    "cancellation",
                    f"Your booking {booking_id} for slot {booking['slot_id']} has been cancelled.",
                    session=session
                )
                
        except Exception:
            return False
        
        return True
    
    async def release_booking(self, booking_id: str, user_id: str):
        booking = await self.get_booking(booking_id, user_id)
        if not booking:
            return False
        
        session = await self.db.client.start_session()
        try:
            async with session.start_transaction():
                # Update booking status
                await self.bookings_collection.update_one(
                    {"booking_id": booking_id},
                    {"$set": {"status": BookingStatus.RELEASED}},
                    session=session
                )
                
                # Free the slot
                await self.slots_collection.update_one(
                    {"slot_id": booking["slot_id"], "parking_id": booking["parking_id"]},
                    {"$set": {
                        "status": "available",
                        "current_booking_id": None
                    }},
                    session=session
                )
                
                # Create notification
                await self.notification_service.create_notification(
                    user_id,
                    "release",
                    f"Slot {booking['slot_id']} at {booking['parking_name']} has been released.",
                    session=session
                )
                
        except Exception:
            return False
        
        return True
