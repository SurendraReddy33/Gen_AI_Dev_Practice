from app.db.mongo_db import user_collection
from app.core.security import encrypt_password, verify_password, generate_auth_token, decode_access_token
from app.models.user_models import Register_Request, Login_Request, Update_Details_Request, Change_Password, Forgot_Password_Request, Verify_Otp_Request
from app.utils.logger import get_logger
from app.utils.email_otp import send_otp_email
from datetime import datetime, timedelta
from fastapi import HTTPException
import bcrypt
import os
 
logger = get_logger(__name__)

email_app_key = os.getenv("App_password")
 
stored_otp = {}

async def register_user(user_data: Register_Request):
    # Check if user already exists
    user_exists = await user_collection.find_one({
        "$or": [
            {"email": user_data.email},
            {"phone_number": user_data.phone_number},
            {"username": user_data.username}
        ]
    })
    if user_exists:
        logger.warning("Duplicate user attempt during registration.")
        raise HTTPException(status_code=400, detail="Email, phone or username already in use.")
 
    # Prepare data
    full_name = f"{user_data.first_name}{user_data.last_name}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    hashed = encrypt_password(user_data.password)
    user_record = {
        "username": user_data.username,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "full_name": full_name,
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
 
    await user_collection.insert_one(user_record)
 
    logger.info(f"New user created: {full_name} with email {user_data.email}")
 
    return {
        "message": "User registered successfully",
        "username": full_name,
        "email": user_data.email
    }
 
async def login_user(data: Login_Request):
    user = await user_collection.find_one({
        "$or": [
            {"email": data.identifier},
            {"username": data.identifier}
        ]
    })
 
    if not user:
        logger.warning(f"Login failed: No Account found for {data.identifier}")
        raise HTTPException(status_code=404, detail="Account not found")
 
    if user["status"] != "Active":
        logger.warning(f"User '{user['username']}' is inactive.")
        raise HTTPException(status_code=403, detail="User is blocked due to multiple failed login attempts")
 
    # Check if password is expired (1 month)
    pwd_created = datetime.strptime(user["password_created_at"], "%Y-%m-%d %H:%M:%S")
    if (datetime.now() - pwd_created).days > 30:
        logger.warning(f"Password expired for '{user['username']}'.")
        raise HTTPException(status_code=403, detail="Password expired. Please update your password.")
 
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
            logger.warning(f"Account with user {user['username']} blocked due to multiple failed login attempts")
        raise HTTPException(status_code=401, detail="Incorrect password")
 
    await user_collection.update_one({"_id": user["_id"]}, {"$set": {"failed_attempts": 0}})

    token = generate_auth_token(user["username"], user["email"])
    logger.info(f"User {user['username']} logged in successfully")
 
    return {
        "message": "Login successful",
        "username": user["username"],
        "token": token
    }

async def update_user(token: str, data: Update_Details_Request):
    payload = decode_access_token(token)
    user_email = payload.get("email")
    if not user_email:
        logger.warning("Invalid token: missing email")
        raise HTTPException(status_code=401, detail="Invalid token: no email found")
 
    existing_user = await user_collection.find_one({"email": user_email})
    if not existing_user:
        logger.warning(f"No user record found for email: {user_email}")
        raise HTTPException(status_code=404, detail="No user found")
 
    if not verify_password(data.password, existing_user["password"]):
        logger.warning(f"Password mismatch for user: {user_email}")
        raise HTTPException(status_code=403, detail="Incorrect password")
 
    if data.username and data.username != existing_user["username"]:
        logger.warning(f"Unauthorized username update attempt by: {user_email}")
        raise HTTPException(status_code=403, detail="Username update not allowed")
 
    updates = {}
    for field in ["username", "first_name", "last_name", "email", "phone_number", "dob", "address"]:
        new_val = getattr(data, field)
        if new_val is not None and new_val != existing_user.get(field):
            updates[field] = new_val
 
    if not updates:
        logger.info(f"No changed detected for user: {user_email}")
        raise HTTPException(status_code=400, detail="No new or changed details provided.")
 
    await user_collection.update_one({"_id": existing_user["_id"]}, {"$set": updates})
    logger.info(f"User details updated for {user_email}: {list(updates.keys())}")
    return {
        "message": "User details updated successfully",
        "username": updates.get("username", existing_user["username"])
    }
 

async def change_password(change_request: Change_Password):
    user = await user_collection.find_one({"email": change_request.email})
    logger.info(f"Password update requested for email: {change_request.email}")

    if not user:
        logger.warning(f"No user found with email: {change_request.email}")
        raise HTTPException(status_code=404, detail=f"{change_request.email} Not Found")
    
    if not verify_password(change_request.old_password, user["password"]):
        logger.warning(f"Incorrect old password provided for user: {change_request.email}")
        raise HTTPException(status_code=401, detail="Old password is incorrect")
    
    new_hashed_password = encrypt_password(change_request.new_password)
    for old_hashed in user['password_history']:
        if verify_password(change_request.new_password, old_hashed):
            logger.warning(f"New password reused from history for user: {change_request.email}")
            raise HTTPException(
                status_code=400,
                detail = "New Password must be different from old passwords"
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
        logger.info(f"Password changed successfully user: {change_request.email}")
    else:
        logger.error(f"Password update failed for user: {change_request.email}")
        raise HTTPException(status_code=500, detail="Failed to update password")
    
    return {"message": "Password updated"}

async def forgot_password(data:Forgot_Password_Request):
    user = await user_collection.find_one({
        "$or": [{"username":data.identifier},{"email":data.identifier}]
    })
    if not user:
        logger.warning(f"No Account matches for: {data.identifier}")
        raise HTTPException(status_code = 404,
                            detail= f"User Not Found")
    otp = send_otp_email(
        receiver_email=user["email"],
        sender_email="gsrgsreddy3@gmail.com",
        app_password=email_app_key
    )
    stored_otp[data.identifier]= {"otp":otp,"expires":datetime.utcnow() + timedelta(minutes=5)}
    logger.info(f"OTP issued to: {data.identifier}")

    return {"message": "otp has been sent to your email"}

async def verify_otp_and_reset_password(data:Verify_Otp_Request):
    record = stored_otp.get(data.identifier)

    if not record:
        logger.warning(f"No OTP found for user: {data.identifier}")
        raise HTTPException(status_code = 404,
                            detail="OTP not Found.")
    if datetime.utcnow()>record["expires"]:
        logger.warning(f"OTP expired for user: {data.identifier}")
        raise HTTPException(status_code =410,
                            detail = "OTP has expired.")
    
    if data.otp!= record["otp"]:
        logger.warning(f"Invalid OTP entered for user: {data.identifier}")
        raise HTTPException(status_code = 404,
                            detail ="Invalid OTP")
    
    hashed_password = encrypt_password(data.new_password)

    await user_collection.update_one(
        {"$or" : [{"username":data.identifier},{"email":data.identifier}]},
        {
            "$set":{"password":hashed_password},
            "$push":{"password_history":hashed_password}
        }
    )

    del stored_otp[data.identifier]
    logger.info(f"Password reset after OTP verification for user: {data.identifier}")

    return {"message" :" OTP Verified and password reset successfully"}