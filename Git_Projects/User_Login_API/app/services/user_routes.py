from fastapi import APIRouter
from app.models.user_models import Register_Request, Register_Response, Login_Request, LoginResponse
from app.services.user_service import register_user,login_user
from app.utils.decorator import handle_exceptions
 
router = APIRouter()

@handle_exceptions
@router.post("/register", response_model=Register_Response)
async def register_user_route(user: Register_Request):
    return await register_user(user)

@handle_exceptions
@router.post("/login")
async def login(login_data: Login_Request):
    return await login_user(login_data)

