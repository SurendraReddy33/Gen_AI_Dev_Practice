from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserResponse, UserLogin, UserUpdate, PasswordChange, ForgotPassword, ResetPassword, Token
from app.services.user_service import UserService
from app.utils.auth import get_current_user, create_access_token
from app.database.mongodb import get_database
from bson import ObjectId
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    db = get_database()
    service = UserService(db)
    
    # Check if user already exists
    if await service.get_user_by_email(user.email):
        raise HTTPException(status_code=409, detail="User with this email already exists")
    
    if await service.get_user_by_username(user.username):
        raise HTTPException(status_code=409, detail="User with this username already exists")
    
    # Create user
    created_user = await service.create_user(user)
    return created_user

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_database()
    service = UserService(db)
    
    # Try to authenticate with email first
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        # If email authentication fails, try username
        user_by_username = await service.get_user_by_username(form_data.username)
        if user_by_username and pwd_context.verify(form_data.password, user_by_username["hashed_password"]):
            user = user_by_username
            # Update last login
            await service.users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": datetime.utcnow()}}
            )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["_id"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    db = get_database()
    service = UserService(db)
    
    user = await service.get_user_by_id(current_user["_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.put("/profile/update")
async def update_user_profile(update_data: UserUpdate, current_user: dict = Depends(get_current_user)):
    db = get_database()
    service = UserService(db)
    
    if not any([update_data.username, update_data.email, update_data.phone]):
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    result = await service.update_user(current_user["_id"], update_data)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "Profile updated successfully"}

@router.delete("/profile/delete")
async def delete_user_account(current_user: dict = Depends(get_current_user)):
    db = get_database()
    service = UserService(db)
    
    result = await service.delete_user(current_user["_id"])
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}

@router.put("/password/change")
async def change_password(password_data: PasswordChange, current_user: dict = Depends(get_current_user)):
    db = get_database()
    service = UserService(db)
    
    result = await service.change_password(current_user["_id"], password_data.old_password, password_data.new_password)
    if not result:
        raise HTTPException(status_code=401, detail="Old password is incorrect")
    
    return {"message": "Password changed successfully"}

@router.post("/password/forgot")
async def forgot_password(forgot_data: ForgotPassword):
    db = get_database()
    service = UserService(db)
    
    user = await service.get_user_by_email(forgot_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    reset_token = await service.generate_reset_token(user["_id"])
    # In production, send email with reset token here
    return {"message": "Password reset token sent to your email", "reset_token": reset_token}

@router.post("/password/reset")
async def reset_password(reset_data: ResetPassword):
    db = get_database()
    service = UserService(db)
    
    result = await service.reset_password(reset_data.reset_token, reset_data.new_password)
    if not result:
        raise HTTPException(status_code=404, detail="Invalid or expired reset token")
    
    return {"message": "Password has been reset successfully"}

@router.post("/logout")
async def logout_user(current_user: dict = Depends(get_current_user)):
    # For JWT, logout is handled client-side by discarding the token
    return {"message": "User logged out successfully"}
