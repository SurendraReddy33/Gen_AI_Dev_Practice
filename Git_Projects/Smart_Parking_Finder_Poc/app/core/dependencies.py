from fastapi import Header, HTTPException, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.security import verify_jwt
from app.db.mongo_db import token_blacklist_collection, login_sessions_collection
from datetime import datetime, timedelta
from app.utils.logger import get_logger

logger = get_logger(__name__)

SESSION_EXP_TIME = 60

async def store_session(email: str, username: str, token: str):    
    session_doc = {
        "email": email,
        "username": username,
        "token": token,
        "created_at": datetime.utcnow(),
        "status": "Active"
    }
    await login_sessions_collection.insert_one(session_doc)
    logger.info(f"Session created for user {username} with email {email}")
 
# ----------------------------
# Remove session on logout
# ----------------------------
async def remove_session(token: str):
    session = await login_sessions_collection.find_one({"token": token})
    if not session:
        logger.warning(f"Logout attempt with invalid or already removed token")
        return "No active session"
 
    # Check if token has expired
    is_expired = datetime.utcnow() > session["created_at"] + timedelta(minutes=SESSION_EXP_TIME)
 
    # Remove session and blacklist the token
    await login_sessions_collection.delete_one({"token": token})
    await token_blacklist_collection.insert_one({
        "token": token,
        "created_at": datetime.utcnow()
    })
 
    if is_expired:
        logger.info(f"Expired token removed and blacklisted: {token}")
        return "Session expired"
    else:
        logger.info(f"User {session['username']} logged out successfully")
        return "Logout successful"

async def validate_token(token: str):
    # 1️⃣ Verify JWT
    try:
        payload = verify_jwt(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_email = payload.get("email")
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token: no email")

    # 2️⃣ Check if token is blacklisted
    if await token_blacklist_collection.find_one({"token": token}):
        raise HTTPException(status_code=403, detail="Token blacklisted")

    # 3️⃣ Check if session exists for this token
    session = await login_sessions_collection.find_one({
        "email": user_email,
        "token": token,
        "status": "Active"
    })
    if not session:
        raise HTTPException(status_code=403, detail="Session not active or logged out")

    # 4️⃣ Optional: check session expiry
    if datetime.utcnow() - session["created_at"] > timedelta(minutes=SESSION_EXP_TIME):
        await login_sessions_collection.update_one(
            {"_id": session["_id"]},
            {"$set": {"status": "expired"}}
        )
        raise HTTPException(status_code=403, detail="Session expired")

    return payload


