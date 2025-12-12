from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CreateBookingRequest(BaseModel):
    lot_id: str
    slot_id: str
    vehicle_type: str

class CreateBookingResponse(BaseModel):
    message: str
    booking_id: str
    lot_id: str
    slot_id: str
    vehicle_type: str
    status: str

class BookingsResponse(BaseModel):
    booking_id: str
    user_email: str
    lot_id: int
    slot_id: str
    vehicle_type: str
    status: str
    created_at: datetime

class BookingByIdResponse(BaseModel):
    booking_id: str
    user_email: str
    lot_id: str
    slot_id: str
    vehicle_type: str
    status: str
    created_at: datetime

class UpdateBookingRequest(BaseModel):
    new_slot_id: Optional[str] = None
    new_vehicle_type: Optional[str] = None

