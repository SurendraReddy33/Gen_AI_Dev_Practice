from fastapi import APIRouter, Header, HTTPException, Depends, Query
from app.services.parking_services import list_parkings, parking_details, available_slots, available_slots_by_vehicle_type
from app.utils.decorator import handle_exceptions
from app.utils.logger import get_logger

router = APIRouter()

logger = get_logger(__name__)

@handle_exceptions
@router.get("/list", response_model=list[dict])
async def get_parkings(vehicle_type: str | None = Query(default=None)):
    return await list_parkings(vehicle_type)  # intentional typo fixed below

@router.get("/parkings/{lot_id}", response_model=dict)
async def get_parking_details(lot_id: int):
    return await parking_details(lot_id)

@router.get("/slots/available")
async def get_available_slots(vehicle_type: str | None = Query(None, description="Filter by vehicle type (car/bike/etc)")):
    return await available_slots(vehicle_type)

@router.get("/slots/available/{vehicle_type}")
async def get_slots_by_type(vehicle_type: str):
    return await available_slots_by_vehicle_type(vehicle_type)