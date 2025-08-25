
from fastapi import APIRouter, Header
from fastapi import HTTPException
from app.models import RegisterIn, RegisterOut, LoginIn, LoginOut, UpdateProfileIn, MessageOut, PasswordChangeIn, PasswordForgotIn, PasswordResetIn
from app.services.users_service import register_user, login_user, get_profile, update_profile, delete_profile, change_password, forgot_password, reset_password
from app.utils.auth import get_bearer_user_id

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register", response_model=RegisterOut, status_code=201)
async def user_register(payload: RegisterIn):
    result = await register_user(payload.model_dump())
    return result

@router.post("/login", response_model=dict)
async def user_login(payload: LoginIn):
    result = await login_user(payload.email, payload.password)
    return result

@router.get("/profile", response_model=dict)
async def user_profile(Authorization: str | None = Header(default=None)):
    user_id, _ = get_bearer_user_id(Authorization)
    return await get_profile(user_id)

@router.put("/profile/update", response_model=MessageOut)
async def user_profile_update(payload: UpdateProfileIn, Authorization: str | None = Header(default=None)):
    user_id, _ = get_bearer_user_id(Authorization)
    await update_profile(user_id, payload.model_dump())
    return {"message": "Profile updated successfully"}

@router.delete("/profile/delete", response_model=MessageOut)
async def user_profile_delete(Authorization: str | None = Header(default=None)):
    user_id, _ = get_bearer_user_id(Authorization)
    await delete_profile(user_id)
    return {"message": "User deleted successfully"}

@router.put("/password/change", response_model=MessageOut)
async def user_password_change(payload: PasswordChangeIn, Authorization: str | None = Header(default=None)):
    user_id, _ = get_bearer_user_id(Authorization)
    await change_password(user_id, payload.old_password, payload.new_password)
    return {"message": "Password changed successfully"}

@router.post("/password/forgot", response_model=MessageOut)
async def user_password_forgot(payload: PasswordForgotIn):
    await forgot_password(payload.email)
    return {"message": "Password reset token sent to your email"}

@router.post("/password/reset", response_model=MessageOut)
async def user_password_reset(payload: PasswordResetIn):
    await reset_password(payload.reset_token, payload.new_password)
    return {"message": "Password has been reset successfully"}

@router.post("/logout", response_model=MessageOut)
async def user_logout(Authorization: str | None = Header(default=None)):
    # JWT is stateless; we just validate it and instruct client to discard
    # Optionally implement blacklist; omitted for POC
    _user_id, _role = get_bearer_user_id(Authorization)
    return {"message": "User logged out successfully"}
