from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import SECRET_KEY
from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
 
password_handler = CryptContext(schemes=["bcrypt"] , deprecated = "auto")

# password handlers
 
def encrypt_password(password:str)->str:
    return password_handler.hash(password)
 
def verify_password(plain: str, hashed: str) -> bool:
    return password_handler.verify(plain,hashed)

def generate_auth_token(username: str, email: str):
    payload = {
        "user": username,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_access_token(token:str):
    try:
        decoded = jwt.decode(token,SECRET_KEY,algorithms = ['HS256'])
        print(decoded)
        return decoded
    except ExpiredSignatureError:
        raise HTTPException(status_code= 401,
                             detail="Token Expired")
    except JWTError:
        raise HTTPException(status_code= 401,
                             detail="Invalid Token")

 


