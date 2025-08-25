from app.models.parking import ParkingLotResponse, ParkingLotDetail, Slot, VehicleType, SlotStatus
from app.database.mongodb import get_database

class ParkingService:
    def __init__(self, db):
        self.db = db
        self.parking_collection = db["parking_lots"]
        self.slots_collection = db["slots"]
    
    async def get_all_parkings(self):
        parkings = await self.parking_collection.find().to_list(None)
        result = []
        
        for parking in parkings:
            total_slots = await self.slots_collection.count_documents({"parking_id": parking["lot_id"]})
            available_slots = await self.slots_collection.count_documents({
                "parking_id": parking["lot_id"],
                "status": "available"
            })
            
            result.append({
                "lot_id": parking["lot_id"],
                "lot_name": parking["lot_name"],
                "location": parking["location"],
                "total_slots": total_slots,
                "available_slots": available_slots,
                "booked_slots": total_slots - available_slots
            })
        
        return result
    
    async def get_parking_with_slots(self, parking_id: str):
        parking = await self.parking_collection.find_one({"lot_id": parking_id})
        if not parking:
            return None
        
        slots = await self.slots_collection.find({"parking_id": parking_id}).to_list(None)
        
        total_slots = len(slots)
        available_slots = sum(1 for slot in slots if slot["status"] == "available")
        
        return {
            "parking_id": parking["lot_id"],
            "lot_name": parking["lot_name"],
            "location": parking["location"],
            "total_slots": total_slots,
            "available_slots": available_slots,
            "booked_slots": total_slots - available_slots,
            "slots": slots
        }
    
    async def get_available_slots(self, parking_id: str, vehicle_type: str = None):
        parking = await self.parking_collection.find_one({"lot_id": parking_id})
        if not parking:
            return None
        
        query = {"parking_id": parking_id, "status": "available"}
        if vehicle_type:
            query["vehicle_type"] = vehicle_type
        
        slots = await self.slots_collection.find(query).to_list(None)
        return slots
