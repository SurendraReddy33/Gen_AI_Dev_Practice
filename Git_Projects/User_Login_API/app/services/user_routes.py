from fastapi import APIRouter, Header
from app.models.user_models import Register_Request, Register_Response, Login_Request, LoginResponse, UpdateDetailsRequest, UpdateDetailsResponse, ChangePassword, ForgotPasswordRequest, VerifyOtpRequest
from app.services.user_service import register_user,login_user, update_user_details, change_password, forgot_password, verify_otp_and_reset_password
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

@handle_exceptions
@router.put("/update", response_model=UpdateDetailsResponse)
async def update_user_route(
    update_data: UpdateDetailsRequest,
    authorization: str = Header(...)
):
    token = authorization.replace("Bearer ", "").strip()
    return await update_user_details(token, update_data)

@handle_exceptions
@router.put("/change_password")
async def change_password_route(change_request: ChangePassword):
    return await change_password(change_request)

@handle_exceptions
@router.post("/Forgot_Password")
async def Forgot_password(data:ForgotPasswordRequest):
    return await forgot_password(data)


@handle_exceptions
@router.post("/verify-otp")
async def otp_verification_reset_password(data:VerifyOtpRequest):
    return await verify_otp_and_reset_password(data)
