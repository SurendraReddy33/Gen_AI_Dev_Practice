from fastapi import APIRouter, HTTPException, Header, Query
from app.core.dependencies import validate_token
from app.services.booking_service import create_booking, list_bookings, get_booking_by_id, release_booking, update_booking
from app.models.booking_models import CreateBookingRequest, CreateBookingResponse, BookingsResponse, BookingByIdResponse, UpdateBookingRequest
from app.utils.logger import get_logger

router = APIRouter()

logger = get_logger(__name__)

@router.post("/create")
async def create_booking_route(
    booking_data: CreateBookingRequest,
    authorization: str = Header(...),
):
    """
    Create a new parking booking (with JWT auth).
    """
    try:
        # ✅ Extract and validate token
        token = authorization.replace("Bearer ", "").strip()
        user = await validate_token(token)  # <-- validate JWT

        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # ✅ Pass user info if you need (e.g., user_id, email)
        result = await create_booking(booking_data, user)

        return result

    except HTTPException as e:
        logger.warning(f"Booking creation failed: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error during booking creation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    

@router.get("/list", response_model=list[BookingsResponse])
async def list_bookings_route(user_email: str | None = Query(default=None)):
    """
    List all bookings, optionally filtered by user email.
    """
    return await list_bookings(user_email)

@router.get("/{booking_id}", response_model=BookingByIdResponse)
async def get_booking_route(booking_id: str):
    return await get_booking_by_id(booking_id)


@router.put("/update/{booking_id}")
async def update_booking_route(booking_id: str, update_data: UpdateBookingRequest):
    try:
        return await update_booking(
            booking_id,
            new_slot_id=update_data.new_slot_id,
            new_vehicle_type=update_data.new_vehicle_type
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error updating booking {booking_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/release/{booking_id}")
async def release_booking_route(booking_id: str):
    return await release_booking(booking_id)





