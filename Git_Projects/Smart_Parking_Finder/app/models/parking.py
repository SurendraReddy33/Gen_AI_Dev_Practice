from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class VehicleType(str, Enum):
    CAR = "car"
    BIKE = "bike"
    SCOOTER = "scooter"

class SlotStatus(str, Enum):
    AVAILABLE = "available"
    BOOKED = "booked"

class Slot(BaseModel):
    slot_id: str
    vehicle_type: VehicleType
    status: SlotStatus
    current_booking_id: Optional[str] = None

class ParkingLotBase(BaseModel):
    lot_name: str
    location: str

class ParkingLotCreate(ParkingLotBase):
    pass

class ParkingLotResponse(ParkingLotBase):
    lot_id: str
    total_slots: int
    available_slots: int
    booked_slots: int

class ParkingLotDetail(ParkingLotResponse):
    slots: List[Slot]

class AvailableSlotsResponse(BaseModel):
    parking_id: str
    available_slots: List[Slot]
    count: int
