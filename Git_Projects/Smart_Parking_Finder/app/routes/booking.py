from fastapi import APIRouter, HTTPException, Depends
from app.models.booking import BookingCreate, BookingResponse, BookingUpdate
from app.services.booking_service import BookingService
from app.utils.auth import get_current_user
from app.database.mongodb import get_database

router = APIRouter()

@router.post("/", response_model=BookingResponse, status_code=201)
async def create_booking(booking_data: BookingCreate, current_user: dict = Depends(get_current_user)):
    db = get_database()
    service = BookingService(db)
    
    booking = await service.create_booking(current_user["_id"], booking_data)
    if not booking:
        raise HTTPException(status_code=400, detail="Cannot create booking")
    
    return booking

@router.get("/", response_model=list[BookingResponse])
async def get_user_bookings(current_user: dict = Depends(get_current_user)):
    db = get_database()
    service = BookingService(db)
    
    bookings = await service.get_user_bookings(current_user["_id"])
    return bookings

@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    service = BookingService(db)
    
    booking = await service.get_booking(booking_id, current_user["_id"])
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return booking

@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(booking_id: str, update_data: BookingUpdate, current_user: dict = Depends(get_current_user)):
    db = get_database()
    service = BookingService(db)
    
    booking = await service.update_booking(booking_id, current_user["_id"], update_data)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found or cannot be updated")
    
    return booking

@router.delete("/{booking_id}")
async def delete_booking(booking_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    service = BookingService(db)
    
    result = await service.cancel_booking(booking_id, current_user["_id"])
    if not result:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return {"message": "Booking cancelled successfully"}

@router.post("/{booking_id}/release")
async def release_booking(booking_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    service = BookingService(db)
    
    result = await service.release_booking(booking_id, current_user["_id"])
    if not result:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return {"message": "Slot released successfully"}
