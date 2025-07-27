from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import SECRET_KEY
from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
 
pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = "auto")
 
def hash_password(password:str)->str:
    return pwd_context.hash(password)
 
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain,hashed)

def create_jwt_token(username: str, email: str):
    payload = {
        "user": username,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt(token:str):
    try:
        decoded = jwt.decode(token,SECRET_KEY,algorithms = ['HS256'])
        return decoded
    except ExpiredSignatureError:
        raise HTTPException(status_code= 401,
                             detail="Token Expired")
    except JWTError:
        raise HTTPException(status_code= 401,
                             detail="Invalid Token")


