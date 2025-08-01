from app.db.mongo_db import user_collection, login_sessions_collection,token_blacklist_collection
from app.core.security import encrypt_password, verify_password, generate_auth_token, decode_access_token
from app.models.user_models import Register_Request, Login_Request, Update_Details_Request, Change_Password,Reset_Password_Otp, Forgot_Password_Request, Verify_Otp_Request
from app.utils.logger import get_logger
from app.utils.email_otp import send_otp_email, send_token
from app.core.dependencies import validate_token, store_session
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
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

    existing_session = await login_sessions_collection.find_one({
        "$or": [
            {"email": user["email"]},
            {"username": user["username"]}
        ]
    })

    if existing_session:
        created_at = existing_session.get("created_at")
        if created_at and (datetime.utcnow() - created_at).total_seconds() < 3600:
            raise HTTPException(status_code=403,
                                detail="You are already logged in. Try again after 1 hour.")
        else:
            await login_sessions_collection.delete_one({"_id": existing_session["_id"]})

    token = generate_auth_token(user["username"], user["email"])
    logger.info(f"User {user['username']} logged in successfully")

    await store_session(user["email"],user["username"],token)
    send_token(
        receiver_email=user["email"],
        sender_email="gsrgsreddy3@gmail.com",
        app_password=email_app_key,
        token=token,
        username=user["username"]
    )
 
    return {
        "message": "Login successful",
        "username": user["username"],
        "token": " Token has been sent to your Registered Mail ID "
    }

async def update_user(token: str, data: Update_Details_Request):
    payload = decode_access_token(token)
    user_email = payload.get("email")
    if not user_email:
        logger.warning("Invalid token: missing email")
        raise HTTPException(status_code=401, detail="Invalid token: no email found")
 
    login_existing_user = await login_sessions_collection.find_one({"email": user_email})
    if not login_existing_user:
        logger.warning(f"No user record found for email: {user_email}")
        raise HTTPException(status_code=404, detail="User Already logged out")
    
    existing_user = await user_collection.find_one({"email": user_email})
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
 
 
async def change_password(token: str, change_request: Change_Password):
    # Step 1: Decode Token
    payload = decode_access_token(token)
    user_email = payload.get("email")
 
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token: no email found")
 
    # Step 2: Check if session is valid
    session = await login_sessions_collection.find_one({"email": user_email, "status": "Active"})
    if not session:
        raise HTTPException(status_code=403, detail="You are not logged in")
 
    if datetime.utcnow() - session["created_at"] > timedelta(hours=1):
        await login_sessions_collection.update_one({"_id": session["_id"]}, {"$set": {"status": "expired"}})
        raise HTTPException(status_code=403, detail="Session expired")
 
    # Step 3: Validate request belongs to same user
    if change_request.email != user_email:
        raise HTTPException(status_code=403, detail="You can only change your own password")
 
    # Step 4: Lookup user
    user = await user_collection.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=404, detail=f"{user_email} Not Found")
 
    # Step 5: Validate old password
    if not verify_password(change_request.old_password, user["password"]):
        raise HTTPException(status_code=401, detail="Old password is incorrect")
 
    # Step 6: Check password reuse
    for old_hashed in user['password_history']:
        if verify_password(change_request.new_password, old_hashed):
            raise HTTPException(status_code=400, detail="New Password must be different from old passwords")
 
    # Step 7: Send OTP
    otp = send_otp_email(
        receiver_email=user["email"],
        sender_email="gsrgsreddy3@gmail.com",
        app_password=email_app_key
    )
 
    stored_otp[user["username"]] = {
        "otp": otp,
        "new_password": change_request.new_password,
        "expires": datetime.utcnow() + timedelta(minutes=5)
    }
 
    return {"message": "OTP has been sent to your registered email"}


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

async def password_reset_with_otp(data : Reset_Password_Otp):
    record = stored_otp.get(data.username)

    if not record:
        logger.warning(f"User not found for username: {data.username}")
        raise HTTPException(status_code=404, detail=f"{data.username} Not Found")
    
    if datetime.utcnow()> record["expires"] :
        logger.info("OTP has been Expired for change_password")
        del stored_otp[data.username]
        raise HTTPException(status_code = 410, detail = "OTP Expired")
    
    if data.otp != record["otp"] :
        logger.info("Invalid OTP ")
        raise HTTPException(status_code = 401,
                            detail = "Invalid OTP")
    
    new_hashed_password = encrypt_password(record["new_password"])

    result = await user_collection.update_one(
        {"username": data.username},
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
        logger.info(f"Password successfully updated for user: {data.username}")
    else:
        logger.error(f"Failed to update password for user: {data.username}")
        raise HTTPException(status_code=500, detail="Failed to update password")
    
    del stored_otp[data.username]

    logger.info(f"Password Changed Successfully for {data.username}")

    return {"message":"OTP verified and password changed successfully"}



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


 
async def logout_user_service(token: str):
    payload = decode_access_token(token)
    email = payload.get("email")
 
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
 
    # Check if token already blacklisted
    existing_blacklisted = await token_blacklist_collection.find_one({"token": token})
    if existing_blacklisted:
        raise HTTPException(status_code=403, detail="Token already blacklisted (Already logged out)")
 
    # Get session for the email
    session = await login_sessions_collection.find_one({"email": email})
    if not session:
        raise HTTPException(status_code=403, detail="Session already expired or not found")
 
    # Optional: check if token in session matches current token
    if session["token"] != token:
        raise HTTPException(status_code=403, detail="Token mismatch – Invalid session")
 
    # Check if session is expired
    session_time = session.get("created_at")
    if not session_time:
        raise HTTPException(status_code=403, detail="Invalid session timestamp")
 
    if datetime.utcnow() - session_time > timedelta(hours=1):
        # Still remove session even if expired
        await login_sessions_collection.delete_one({"email": email})
        await token_blacklist_collection.insert_one({
            "token": token,
            "email": email,
            "blacklisted_at": datetime.utcnow(),
            "expires_at": datetime.utcfromtimestamp(payload.get("exp", datetime.utcnow().timestamp() + 3600))
        })
        return {"message": "Session already expired. Token blacklisted."}
 
    # All good: logout now
    await login_sessions_collection.delete_one({"email": email})
 
    await token_blacklist_collection.insert_one({
        "token": token,
        "email": email,
        "blacklisted_at": datetime.utcnow(),
        "expires_at": datetime.utcfromtimestamp(payload.get("exp", datetime.utcnow().timestamp() + 3600))
    })
 
    return {"message": "Logout successful"}

