from fastapi import APIRouter
from app.models.user_models import Register_Request, Register_Response
from app.services.user_service import register_user
 
router = APIRouter()
 
@router.post("/register", response_model=Register_Response)
def register_user_route(user: Register_Request):
    return register_user(user)