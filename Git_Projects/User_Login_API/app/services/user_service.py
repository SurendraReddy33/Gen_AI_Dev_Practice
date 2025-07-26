from app.db.mongo_db import user_collection
from app.core.security import hash_password, verify_password, create_jwt_token
from app.models.user_models import Register_Request, Login_Request
from app.utils.logger import get_logger
from datetime import datetime, timedelta
from fastapi import HTTPException
 
logger = get_logger(__name__) 

def register_user(user_data: Register_Request):
    # Check if user already exists
    existing_user = user_collection.find_one({
        "$or": [
            {"email": user_data.email},
            {"phone_number": user_data.phone_number},
            {"username": user_data.username}
        ]
    })
    if existing_user:
        raise HTTPException(status_code=400, detail="User with given email, phone number, or username already exists")
 
    # Prepare data
    full_username = f"{user_data.first_name}{user_data.last_name}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_doc = {
        "username": user_data.username,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "full_name": full_username,
        "email": user_data.email,
        "phone_number": user_data.phone_number,
        "password": hash_password(user_data.password),
        "dob": user_data.dob,
        "doj": user_data.doj,
        "address": user_data.address,
        "status": "Active",
        "password_created_at": timestamp,
        "failed_attempts": 0
    }
 
    user_collection.insert_one(user_doc)
 
    logger.info(f"User {full_username} registered with email: {user_data.email}")
 
    return {
        "message": "User registered successfully",
        "username": full_username,
        "email": user_data.email
    }
 
def login_user(login_data: Login_Request):
    user = user_collection.find_one({
        "$or": [
            {"email": login_data.identifier},
            {"username": login_data.identifier}
        ]
    })
 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
 
    if user["status"] == "Blocked":
        raise HTTPException(status_code=403, detail="User is blocked due to multiple failed login attempts")
 
    # Check if password is expired (1 month)
    password_created_at = datetime.strptime(user["password_created_at"], "%Y-%m-%d %H:%M:%S")
    if password_created_at < datetime.now() - timedelta(days=30):
        raise HTTPException(status_code=403, detail="Your password has expired. Please change your password and try again.")
 
    # Verify password
    if not verify_password(login_data.password, user["password"]):
        user_collection.update_one({"_id": user["_id"]}, {"$inc": {"failed_attempts": 1}})
        if user["failed_attempts"] + 1 >= 3:
            user_collection.update_one({"_id": user["_id"]}, {"$set": {"status": "Blocked"}})
            logger.warning(f"User {user['username']} blocked due to multiple failed login attempts")
            raise HTTPException(status_code=403, detail="User blocked due to multiple failed attempts")
        raise HTTPException(status_code=401, detail="Incorrect password")
 
    user_collection.update_one({"_id": user["_id"]}, {"$set": {"failed_attempts": 0}})
    token = create_jwt_token(user["username"], user["email"], expiry_minutes=60)
    logger.info(f"User {user['username']} logged in successfully")
 
    return {
        "message": "Login successful",
        "username": user["username"],
        "token": token
    }
