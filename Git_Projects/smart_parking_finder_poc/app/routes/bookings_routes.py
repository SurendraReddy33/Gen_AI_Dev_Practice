
from fastapi import APIRouter, Header
from app.models import CreateBookingIn
from app.services.bookings_service import create_booking, list_bookings, get_booking, update_booking, delete_booking, release_booking
from app.utils.auth import get_bearer_user_id

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("", response_model=dict, status_code=201)
async def create_booking_route(payload: CreateBookingIn, Authorization: str | None = Header(default=None)):
    user_id, _ = get_bearer_user_id(Authorization)
    return await create_booking(user_id, payload.parking_id, payload.slot_id, payload.vehicle_type)

@router.get("", response_model=list[dict])
async def list_bookings_route(Authorization: str | None = Header(default=None)):
    user_id, _ = get_bearer_user_id(Authorization)
    return await list_bookings(user_id)

@router.get("/{booking_id}", response_model=dict)
async def get_booking_route(booking_id: str, Authorization: str | None = Header(default=None)):
    user_id, _ = get_bearer_user_id(Authorization)
    return await get_booking(user_id, booking_id)

@router.put("/{booking_id}", response_model=dict)
async def update_booking_route(booking_id: str, payload: dict, Authorization: str | None = Header(default=None)):
    user_id, _ = get_bearer_user_id(Authorization)
    return await update_booking(user_id, booking_id, payload.get("slot_id"), payload.get("vehicle_type"))

@router.delete("/{booking_id}", response_model=dict)
async def delete_booking_route(booking_id: str, Authorization: str | None = Header(default=None)):
    user_id, _ = get_bearer_user_id(Authorization)
    return await delete_booking(user_id, booking_id)

@router.post("/{booking_id}/release", response_model=dict)
async def release_booking_route(booking_id: str, Authorization: str | None = Header(default=None)):
    user_id, _ = get_bearer_user_id(Authorization)
    return await release_booking(user_id, booking_id)
