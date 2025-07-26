from fastapi import APIRouter
from app.models.user_models import Register_Request, Register_Response, Login_Request
from app.services.user_service import register_user, login_user
 
router = APIRouter()
 
@router.post("/register", response_model=Register_Response)
def register_user_route(user: Register_Request):
    return register_user(user)

@router.post("/login")
def login(login_data: Login_Request):
    return login_user(login_data)