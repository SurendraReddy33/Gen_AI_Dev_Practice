from pydantic import BaseModel, EmailStr, Field, validator
from fastapi import HTTPException
from typing import Optional
from app.utils.logger import get_logger
import re

logger = get_logger(__name__)

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
    def validate_gmail(cls, mail):
         if not mail.endswith("@gmail.com"):
            logger.warning("Signup Blocked due to unsupported domain: %s", mail)
            raise HTTPException(status_code = 400,
                                detail = "Invalid Email")
         return mail
    
    @validator('password')
    def validate_password(cls, mail):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!#%*?&]{8,20}$', mail):
            logger.warning("Password requirement does not matched")
            raise HTTPException(status_code =400,
                                detail = "Password must be 8-20 chars, include uppercase, lowercase, number, special char")
        return mail
    
class Register_Response(BaseModel):
    message : str
    username : str
    email : str

class Login_Request(BaseModel):
    identifier: str  # email or username
    password: str

class Login_Response(BaseModel):
    message: str
    username: str
    token: str

class Update_Details_Request(BaseModel):
    password: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[int] = None
    dob: Optional[str] = None
    address: Optional[str] = None

class Update_Details_Response(BaseModel):
    message: str
    username: str

class Change_Password(BaseModel):
    email: str
    old_password: str
    new_password: str

class Forgot_Password_Request(BaseModel):
    identifier: str
 
class Verify_Otp_Request(BaseModel):
    identifier: str
    otp: str
    new_password: str
 







