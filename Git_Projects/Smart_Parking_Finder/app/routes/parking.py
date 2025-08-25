from fastapi import APIRouter, HTTPException
from app.models.parking import ParkingLotResponse, ParkingLotDetail, AvailableSlotsResponse
from app.services.parking_service import ParkingService
from app.database.mongodb import get_database

router = APIRouter()

@router.get("/", response_model=list[ParkingLotResponse])
async def get_all_parkings():
    db = get_database()
    service = ParkingService(db)
    
    parkings = await service.get_all_parkings()
    return parkings

@router.get("/{parking_id}", response_model=ParkingLotDetail)
async def get_parking_details(parking_id: str):
    db = get_database()
    service = ParkingService(db)
    
    parking = await service.get_parking_with_slots(parking_id)
    if not parking:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    
    return parking

@router.get("/{parking_id}/slots", response_model=ParkingLotDetail)
async def get_all_slots(parking_id: str):
    db = get_database()
    service = ParkingService(db)
    
    parking = await service.get_parking_with_slots(parking_id)
    if not parking:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    
    return parking

@router.get("/{parking_id}/slots/available", response_model=AvailableSlotsResponse)
async def get_available_slots(parking_id: str, vehicle_type: str = None):
    db = get_database()
    service = ParkingService(db)
    
    available_slots = await service.get_available_slots(parking_id, vehicle_type)
    if available_slots is None:
        raise HTTPException(status_code=404, detail="Parking lot not found")
    
    return {
        "parking_id": parking_id,
        "available_slots": available_slots,
        "count": len(available_slots)
    }
