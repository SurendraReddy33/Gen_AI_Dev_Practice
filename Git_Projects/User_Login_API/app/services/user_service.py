from app.db.mongo_db import user_collection
from app.core.security import hash_password, verify_password, create_jwt_token, verify_jwt
from app.models.user_models import Register_Request, Login_Request, UpdateDetailsRequest, ChangePassword
from app.utils.logger import get_logger
from datetime import datetime, timedelta
from fastapi import HTTPException
import bcrypt
import os
 
logger = get_logger(__name__) 

async def register_user(user_data: Register_Request):
    # Check if user already exists
    existing_user = await user_collection.find_one({
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

    hashed = hash_password(user_data.password)
    user_doc = {
        "username": user_data.username,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "full_name": full_username,
        "email": user_data.email,
        "phone_number": user_data.phone_number,
        "password": hashed,
        "dob": user_data.dob,
        "doj": user_data.doj,
        "address": user_data.address,
        "status": "Active",
        "password_history": [hashed],
        "password_created_at": timestamp,
        "failed_attempts": 0
    }
 
    await user_collection.insert_one(user_doc)
 
    logger.info(f"User {full_username} registered with email: {user_data.email}")
 
    return {
        "message": "User registered successfully",
        "username": full_username,
        "email": user_data.email
    }
 
async def login_user(data: Login_Request):
    user = await user_collection.find_one({
        "$or": [
            {"email": data.username_or_email},
            {"username": data.username_or_email}
        ]
    })
 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
 
    if user["status"] != "Active":
        raise HTTPException(status_code=403, detail="User is blocked due to multiple failed login attempts")
 
    # Check if password is expired (1 month)
    pwd_created = datetime.strptime(user["password_created_at"], "%Y-%m-%d %H:%M:%S")
    if (datetime.now() - pwd_created).days > 30:
        raise HTTPException(status_code=403, detail="Password expired. Please change your password and try again.")
 
    # Verify password
    if not verify_password(data.password, user["password"]):
        await user_collection.update_one({"_id": user["_id"]}, {"$inc": {"failed_attempts": 1}})
        if user["failed_attempts"] + 1 >= 3:
            await user_collection.update_one({"_id": user["_id"]}, {
                "$set": {
                    "status": "Inactive",
                    "inactive_until": datetime.now() + timedelta(hours=24)
                }
            })
            logger.warning(f"User {user['username']} blocked due to multiple failed login attempts")
        raise HTTPException(status_code=401, detail="Incorrect password")
 
    await user_collection.update_one({"_id": user["_id"]}, {"$set": {"failed_attempts": 0}})

    token = create_jwt_token(user["username"], user["email"])
    logger.info(f"User {user['username']} logged in successfully")
 
    return {
        "message": "Login successful",
        "username": user["username"],
        "token": token
    }

async def update_user_details(token: str, data: UpdateDetailsRequest):
    payload = verify_jwt(token)
    logged_in_email = payload.get("email")
    if not logged_in_email:
        raise HTTPException(status_code=401, detail="Invalid token: no email found")
 
    user = await user_collection.find_one({"email": logged_in_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
 
    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=403, detail="Incorrect password")
 
    if data.username and data.username != user["username"]:
        raise HTTPException(status_code=403, detail="You can only update your own account")
 
    updates = {}
    for field in ["username", "first_name", "last_name", "email", "phone_number", "dob", "address"]:
        new_val = getattr(data, field)
        if new_val is not None and new_val != user.get(field):
            updates[field] = new_val
 
    if not updates:
        raise HTTPException(status_code=400, detail="No new details provided or same as existing.")
 
    await user_collection.update_one({"_id": user["_id"]}, {"$set": updates})
    logger.info(f"User {logged_in_email} updated details: {list(updates.keys())}")
    return {
        "message": "Details updated successfully",
        "username": updates.get("username", user["username"])
    }
 

async def change_password(change_request: ChangePassword):
    user = await user_collection.find_one({"email": change_request.email})
    logger.info(f"Password change requested for email: {change_request.email}")

    if not user:
        logger.warning(f"User not found for email: {change_request.email}")
        raise HTTPException(status_code=404, detail=f"{change_request.email} Not Found")
    
    if not verify_password(change_request.old_password, user["password"]):
        logger.warning(f"Incorrect old pasword for user: {change_request.email}")
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    
    new_hashed_password = hash_password(change_request.new_password)
    for old_hashed in user['password_history']:
        if verify_password(change_request.new_password, old_hashed):
            raise HTTPException(
                status_code=400,
                detail = "New Password must not match any of the previous passwords"
            )
    
    result = await user_collection.update_one(
        {"email": change_request.email},
        {
            "$set": {
                "password": new_hashed_password,
                "password_created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "$push": {
                "password_history": new_hashed_password
            }
        }
    )

    if result.modified_count == 1:
        logger.info(f"Password successfully updated for user: {change_request.email}")
    else:
        logger.error(f"Failed to update password for user: {change_request.email}")
        raise HTTPException(status_code=500, detail=" Failed to update password")
    
    return {"message": "Password changed successfully"}