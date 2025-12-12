from typing import List
from fastapi import APIRouter, Header, HTTPException, Depends, Query
from app.services.parking_services import list_parkings_service, parking_details, available_slots, available_slots_by_vehicle_type
from app.utils.decorator import handle_exceptions
from app.models.parking_models import ParkingLotResponse
from app.utils.logger import get_logger
from app.core.security import verify_jwt
from app.core.dependencies import validate_token

router = APIRouter()

logger = get_logger(__name__)

@router.get("/list", response_model=ParkingLotResponse)
async def get_parkings(
    authorization: str = Header(...),
    vehicle_type: str | None = Query(default=None)
):
    """
    List all parking lots. Optional filter by vehicle_type.
    Requires Authorization header: Bearer <token>
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.replace("Bearer ", "").strip()

    parkings_list = await list_parkings_service(token, vehicle_type)
    
    return {"parkings": parkings_list}

@router.get("/parkings/{lot_id}", response_model=dict)
async def get_parking_details(
    lot_id: int,
    authorization: str = Header(...),
):  
    logger.info("Parkings List requested.")

    # ✅ Extract and validate token
    token = authorization.replace("Bearer ", "").strip()
    user = await validate_token(token)  # <-- validate JWT

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # ✅ Pass only lot_id to service
    return await parking_details(lot_id)

@router.get("/slots/available")
async def get_available_slots(
    authorization: str = Header(...),
    vehicle_type: str | None = Query(None, description="Filter by vehicle type (car/bike/etc)")
):  

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.replace("Bearer ", "").strip()

    user = await validate_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return await available_slots(vehicle_type)

@router.get("/slots/available/", response_model = dict)
async def get_available_slots(
    authorization: str = Header(...),
    vehicle_type: str | None = Query(None, description="Filter by vehicle type (car/bike/etc)")
):  
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.replace("Bearer ", "").strip()

    user = await validate_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return await available_slots_by_vehicle_type(vehicle_type)