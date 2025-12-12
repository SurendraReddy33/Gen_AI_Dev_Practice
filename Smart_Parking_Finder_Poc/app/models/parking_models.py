from pydantic import BaseModel, EmailStr, Field, validator
from fastapi import HTTPException
from typing import List, Literal, Optional
from app.utils.logger import get_logger
import re

logger = get_logger(__name__)


class ParkingLotItem(BaseModel):
    lot_id: int
    lot_name: str
    location: str
    total_slots: int
    available_slots: int
    booked_slots: int

class ParkingLotResponse(BaseModel):
    parkings: List[ParkingLotItem]

class Slot(BaseModel):
    slot_id: str
    vehicle_type: Literal["car", "bike", "scooter"] | str = "car"
    status: Literal["available", "booked"] = "available"
    current_booking_id: Optional[str] = None

class ParkingDetailsOut(BaseModel):
    lot_id: int
    lot_name: str
    total_slots: int
    available_slots: int
    booked_slots: int
    slots: list[Slot]

class SlotsOut(BaseModel):
    lot_id: int
    lot_name: str
    total_slots: int
    slots: list[Slot]

class AvailableSlotsOut(BaseModel):
    lot_id: int
    available_slots: list[Slot]
    count: int

# Response model for available slots
class AvailableSlotResponse(BaseModel):
    lot_id: int
    lot_name: str
    slot_id: str
    vehicle_type: str
    status: str


# Wrapper for list response
class AvailableSlotsResponse(BaseModel):
    available_slots: List[AvailableSlotResponse]
    count: int

class VehicleTypeRequest(BaseModel):
    vehicle_type: Literal["car", "bike", "truck"] 
