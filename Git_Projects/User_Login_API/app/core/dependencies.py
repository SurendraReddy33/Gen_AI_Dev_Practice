from fastapi import Header, HTTPException, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.security import decode_access_token
from app.db.mongo_db import token_blacklist_collection, login_sessions_collection
from datetime import datetime, timedelta
from app.utils.logger import get_logger

logger = get_logger(__name__)

SESSION_EXP_TIME = 60

# session handlers

async def store_session(email: str, username: str, token: str):
    # Remove any old sessions beyond expiry duration
    await login_sessions_collection.delete_many({
        "email": email,
        "created_at": {
            "$lt": datetime.utcnow() - timedelta(minutes=SESSION_EXP_TIME)
        }
    })
    # Check if an active session already exists
    existing = await login_sessions_collection.find_one({"email": email})
    if existing:
        logger.warning(f"Attempted login while active session exists for {email}")
        raise HTTPException(status_code=410, detail="Active session exists. Please logout or wait till it expires.")
    
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
 
 
async def validate_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    token = authorization.split(" ")[1]
    try:
        payload = decode_access_token(token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has Expired")
    except JWTError as e:
        print("JWTError:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")
 
    # Check if token is blacklisted
    if await token_blacklist_collection.find_one({"token": token}):
        raise HTTPException(status_code=403, detail="Token blacklisted")
 
    # Check login session is valid
    user_email = payload.get("email")
    print(user_email)
    session = await login_sessions_collection.find_one({"email": user_email, "status": "Active"})
    if not session:
        raise HTTPException(status_code=403, detail="You are not logged in")
 
    if datetime.utcnow() - session["created_at"] > timedelta(hours=1):
        await login_sessions_collection.update_one({"_id": session["_id"]}, {"$set": {"status": "expired"}})
        raise HTTPException(status_code=403, detail="Session expired")
 
    return payload