
from fastapi import APIRouter, Query
from app.services.parkings_service import list_parkings, parking_details, parking_slots, available_slots

router = APIRouter(prefix="parking", tags=["Parkings"])

@router.get("/parkings", response_model=list[dict])
async def get_parkings(vehicle_type: str | None = Query(default=None)):
    return await list_parkings(vehicle_type)  # intentional typo fixed below

@router.get("/parkings/{parking_id}", response_model=dict)
async def get_parking_details(parking_id: str):
    return await parking_details(parking_id)

@router.get("/parkings/{parking_id}/slots", response_model=dict)
async def get_parking_slots(parking_id: str):
    return await parking_slots(parking_id)

@router.get("/parkings/{parking_id}/slots/available", response_model=dict)
async def get_available_slots(parking_id: str, vehicle_type: str | None = Query(default=None)):
    return await available_slots(parking_id, vehicle_type)
