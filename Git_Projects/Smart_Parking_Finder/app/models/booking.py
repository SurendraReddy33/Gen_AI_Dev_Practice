from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.parking import VehicleType

class BookingStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    RELEASED = "released"

class BookingBase(BaseModel):
    parking_id: str
    slot_id: str
    vehicle_type: VehicleType

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    booking_id: str
    user_id: str
    status: BookingStatus
    created_at: datetime
    parking_name: str

class BookingUpdate(BaseModel):
    slot_id: Optional[str] = None
    vehicle_type: Optional[VehicleType] = None
