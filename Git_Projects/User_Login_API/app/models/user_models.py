from pydantic import BaseModel, EmailStr, Field, validator
from fastapi import HTTPException
from typing import Optional
import re

class Register_Request(BaseModel):
    first_name : str
    last_name : str
    username : str
    email : EmailStr
    phone_number : int
    password : str
    dob : str
    doj : str
    address : str

    @validator('email')
    def validate_gmail(cls, v):
         if not v.endswith("@gmail.com"):
            raise HTTPException(status_code = 400,
                                detail = "Invalid Email")
         return v
    
    @validator('password')
    def validate_password(cls, v):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!#%*?&]{8,20}$', v):
            raise HTTPException(status_code =400,
                                detail = "Password must be 8-20 chars, include uppercase, lowercase, number, special char")
        return v
    
class Register_Response(BaseModel):
    message : str
    username : str
    email : str

class Login_Request(BaseModel):
    username_or_email: str  # email or username
    password: str

class LoginResponse(BaseModel):
    message: str
    username: str
    token: str

class UpdateDetailsRequest(BaseModel):
    password: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[int] = None
    dob: Optional[str] = None
    address: Optional[str] = None

class UpdateDetailsResponse(BaseModel):
    message: str
    username: str

class ChangePassword(BaseModel):
    email: str
    old_password: str
    new_password: str

class ForgotPasswordRequest(BaseModel):
    username_or_email: str
 
class VerifyOtpRequest(BaseModel):
    username_or_email: str
    otp: str
    new_password: str
 
class ResetPasswordRequest(BaseModel):
    username_or_email: str
    new_password: str
 
class GenericResponse(BaseModel):
    message: str







