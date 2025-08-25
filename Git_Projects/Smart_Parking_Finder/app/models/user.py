from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
import re
from app.utils.validators import validate_password_complexity

class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone: str

class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_validator(cls, v):
        validate_password_complexity(v)
        return v

    @validator('phone')
    def phone_validator(cls, v):
        if not re.match(r'^\d{10}$', v):
            raise ValueError('Phone must be 10 digits')
        return v

class UserResponse(UserBase):
    id: str
    created_at: datetime
    is_active: bool
    role: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    reset_token: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str
