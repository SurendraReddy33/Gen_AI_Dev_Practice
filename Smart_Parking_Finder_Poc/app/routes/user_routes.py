from fastapi import APIRouter, Header, HTTPException, Depends
from app.models.user_models import Register_Request, Register_Response, Login_Request, Login_Response, Update_Details_Request, Update_Details_Response, Change_Password, Reset_Password_Otp,Forgot_Password_Request, Verify_Otp_Request
from app.services.user_service import register_user,login_user, update_user, change_password, password_reset_with_otp,forgot_password, verify_otp_and_reset_password, logout_user_service
from app.utils.decorator import handle_exceptions
from app.utils.logger import get_logger
 
router = APIRouter()

logger = get_logger(__name__)

@handle_exceptions
@router.post("/register", response_model=Register_Response)
async def signup(user: Register_Request):
    logger.info("New Registration attempt initiated.")
    return await register_user(user)

@handle_exceptions
@router.post("/login", response_model=Login_Response)
async def login(data: Login_Request):
    logger.info("Login initiated for: %s", data.identifier)
    return await login_user(data)

@handle_exceptions
@router.put("/update", response_model=Update_Details_Response)
async def update_user_route(
    update_data: Update_Details_Request,
    authorization: str = Header(...)
):  
    logger.info("User profile update requested.")
    token = authorization.replace("Bearer ", "").strip()
    return await update_user(token, update_data)

@handle_exceptions
@router.put("/change_password")
async def change_password_route(change_request: Change_Password, authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization[len("Bearer "):].strip()
    logger.info("Password change request received.")
    return await change_password(token, change_request)

@handle_exceptions
@router.post("/change_password/otp")
async def change_password_otp_route(data : Reset_Password_Otp):
    return await password_reset_with_otp(data)

@handle_exceptions
@router.post("/Forgot_Password")
async def Forgot_password_route(data:Forgot_Password_Request):
    logger.info("Forgot password trigerred for: %s", data.identifier)
    return await forgot_password(data)


@handle_exceptions
@router.post("/verify_otp")
async def verify_otp(data:Verify_Otp_Request):
    logger.info("OTP verification and password reset initiated.")
    return await verify_otp_and_reset_password(data)


@handle_exceptions
@router.post("/logout")
async def logout_route(authorization: str= Header(...)):
    token = authorization.replace("Bearer ", "").strip()
    return await logout_user_service(token)

