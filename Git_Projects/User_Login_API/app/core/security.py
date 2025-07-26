from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.core.config import SECRET_KEY
 
pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = "auto")
 
def hash_password(password:str)->str:
    return pwd_context.hash(password)
 
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain,hashed)

def create_jwt_token(username: str, email: str, expiry_minutes: int = 60):
    payload = {
        "sub": username,
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=expiry_minutes)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


