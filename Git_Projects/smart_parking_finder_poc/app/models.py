
import re
from typing import Optional, Literal, Any
from fastapi import HTTPException
from pydantic import BaseModel, Field, EmailStr, validator 
from datetime import datetime

# ---------- Pydantic Models (DTOs) ----------

class RegisterIn(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: str

    
    @validator('email')
    def validate_gmail(cls, mail):
         if not mail.endswith("@gmail.com"):
            raise HTTPException(status_code = 400,
                                detail = "Invalid Email")
         return mail
    
    @validator('password')
    def validate_password(cls, mail):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!#%*?&]{8,20}$', mail):
            raise HTTPException(status_code =400,
                                detail = "Password must be 8-20 chars, include uppercase, lowercase, number, special char")
        return mail

class RegisterOut(BaseModel):
    id: str
    username: str
    email: str
    phone: str
    message: str = "User registered successfully"

class LoginIn(BaseModel):
    email: str
    password: str

class LoginOut(BaseModel):
    status: str
    message: str
    user: dict

class UpdateProfileIn(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class MessageOut(BaseModel):
    message: str

class PasswordChangeIn(BaseModel):
    old_password: str
    new_password: str

class PasswordForgotIn(BaseModel):
    email: str

class PasswordResetIn(BaseModel):
    reset_token: str
    new_password: str

# Parking related
class ParkingOut(BaseModel):
    lot_id: str
    lot_name: str
    location: Optional[str] = None
    total_slots: int
    available_slots: int
    booked_slots: int

class Slot(BaseModel):
    slot_id: str
    vehicle_type: Literal["car", "bike", "scooter"] | str = "car"
    status: Literal["available", "booked"] = "available"
    current_booking_id: Optional[str] = None

class ParkingDetailsOut(BaseModel):
    parking_id: str
    lot_name: str
    total_slots: int
    available_slots: int
    booked_slots: int
    slots: list[Slot]

class SlotsOut(BaseModel):
    parking_id: str
    lot_name: str
    total_slots: int
    slots: list[Slot]

class AvailableSlotsOut(BaseModel):
    parking_id: str
    available_slots: list[Slot]
    count: int

# Bookings
class CreateBookingIn(BaseModel):
    parking_id: str
    slot_id: str
    vehicle_type: str

class BookingOut(BaseModel):
    booking_id: str
    user_id: str
    parking_id: str
    slot_id: str
    vehicle_type: str
    status: Literal["active", "cancelled", "released"] = "active"
    created_at: datetime
    message: Optional[str] = None

# Notifications
class NotificationOut(BaseModel):
    notification_id: str
    type: str
    message: str
    status: Literal["unread", "read"] = "unread"
    created_at: datetime

# ---------- Mongo helpers (collection names) ----------

USERS_COLL = "users"
PARKINGS_COLL = "parking_lots"
SLOTS_COLL = "slots"
BOOKINGS_COLL = "bookings"
NOTIFS_COLL = "notifications"
