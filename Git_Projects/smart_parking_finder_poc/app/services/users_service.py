
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, Header, status
from bson import ObjectId
import uuid

import jwt
from app.config.db import get_db
from app.models import USERS_COLL
from app.utils.validators import validate_email, validate_phone, validate_password
from app.utils.auth import hash_password, verify_password, generate_jwt
from app.config.settings import settings
from app.utils.emailer import send_mail
 


def _oid_str(oid) -> str:
    return str(oid) if isinstance(oid, ObjectId) else oid

async def register_user(data: dict) -> dict:
    db = get_db()
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    phone = (data.get("phone") or "").strip()

    if not username:
        raise HTTPException(status_code=400, detail="Username must not be empty")
    validate_email(email)
    validate_password(password)
    validate_phone(phone)

    # Check duplicates
    dup = await db[USERS_COLL].find_one({"$or": [{"email": email}, {"username": username}]})
    if dup:
        if dup.get("email") == email:
            raise HTTPException(status_code=409, detail="User with this email already exists")
        else:
            raise HTTPException(status_code=409, detail="Username already exists")

    hashed = hash_password(password)
    user_doc = {
        "username": username,
        "email": email,
        "phone": phone,
        "password_hash": hashed,
        "role": "user",
        "created_at": datetime.utcnow(),
        "is_active": True,
        "reset_token": None,
        "reset_token_created_at": None,
        "last_login": None,
    }
    res = await db[USERS_COLL].insert_one(user_doc)
    return {
        "id": _oid_str(res.inserted_id),
        "username": username,
        "email": email,
        "phone": phone,
        "message": "User registered successfully",
    }


async def login_user(email: str, password: str) -> dict:
    db = get_db()
    user = await db[USERS_COLL].find_one({"email": email.lower()})
    if not user:
        raise HTTPException(status_code=404, detail="User not found with this email")

    if not verify_password(password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid password")

    # Check existing active session
    existing_session = await db["login_sessions"].find_one({
        "user_id": str(user["_id"]),
        "is_active": True,
        "expiry_time": {"$gt": datetime.utcnow()}
    })
    
            
    if existing_session:
        # ✅ FIX: await the session query
        session = await db["login_sessions"].find_one({"user_id": str(user["_id"])})

        expiry_time = session.get("expiry_time")
        if not expiry_time:
            raise HTTPException(status_code=401, detail="Invalid session expiry")

        if datetime.utcnow() > expiry_time:
        # Expired → mark inactive
            db.login_sessions.update_one(
            {"_id": session["_id"]},
            {"$set": {"is_active": False}}
        )
            raise HTTPException(status_code=401, detail="Session expired, login again")

        if not session.get("is_active", False):
            raise HTTPException(status_code=401, detail="Inactive session, login again")

        raise HTTPException(status_code=403, detail="User already logged in")


    # Generate token
    token = generate_jwt(str(user["_id"]), user.get("role", "user"))

    # Insert session with expiry
    await db["login_sessions"].insert_one({
        "user_id": str(user["_id"]),
        "token": token,
        "login_time": datetime.utcnow(),
        "expiry_time": datetime.utcnow() + timedelta(hours=1),
        "is_active": True
    })

    # Update last login
    await db[USERS_COLL].update_one(
        {"_id": user["_id"]}, {"$set": {"last_login": datetime.utcnow()}}
    )

    return {
        "status": "success",
        "message": "Login successful",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "role": user.get("role", "user"),
        },
    }



# async def login_user(email: str, password: str) -> dict:
#     db = get_db()
#     user = await db[USERS_COLL].find_one({"email": email.lower()})
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found with this email")

#     if not verify_password(password, user.get("password_hash", "")):
#         raise HTTPException(status_code=401, detail="Invalid password")

#     user_id_str = str(user["_id"])
#     now = datetime.utcnow()

#     # 1) Deactivate any expired sessions first (so stale 'is_active: true' doesn't block login)
#     await db["login_sessions"].update_many(
#         {
#             "user_id": user_id_str,
#             "is_active": True,
#             "expiry_time": {"$lte": now},
#         },
#         {"$set": {"is_active": False}}
#     )

#     # 2) Check for an actually-active session (still within expiry window)
#     existing_session = await db["login_sessions"].find_one({
#         "user_id": user_id_str,
#         "is_active": True,
#         "expiry_time": {"$gt": now}
#     })
#     if existing_session:
#         raise HTTPException(status_code=403, detail="User already logged in")

#     # 3) Create new session
#     token = generate_jwt(user_id_str, user.get("role", "user"))
#     await db["login_sessions"].insert_one({
#         "user_id": user_id_str,
#         "token": token,
#         "login_time": now,
#         "expiry_time": now + timedelta(hours=1),
#         "is_active": True
#     })

#     # 4) Update last login
#     await db[USERS_COLL].update_one(
#         {"_id": user["_id"]},
#         {"$set": {"last_login": now}}
#     )

#     return {
#         "status": "success",
#         "message": "Login successful",
#         "token": token,
#         "user": {
#             "id": user_id_str,
#             "email": user["email"],
#             "role": user.get("role", "user"),
#         },
#     }


async def get_user_from_token(token: str):
    """Check token validity (JWT + session) and return user if active"""
    db = get_db()

    try:
        # ✅ Decode token first
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        user_id = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired, login again")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")

    # ✅ Now check session in DB
    session = await db.login_sessions.find_one({"token": token})
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session token")

    expiry_time = session.get("expiry_time")
    if not expiry_time:
        raise HTTPException(status_code=401, detail="Invalid session expiry")

    now = datetime.utcnow()
    if now > expiry_time:
        # Expired → mark inactive
        await db.login_sessions.update_one(
            {"_id": session["_id"]},
            {"$set": {"is_active": False}}
        )
        raise HTTPException(status_code=401, detail="Session expired, login again")

    if not session.get("is_active", False):
        raise HTTPException(status_code=401, detail="Inactive session, login again")

    # ✅ Fetch user by ID from token/session
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def update_profile(user_id: str, data: dict, authorization: str):
    """
    Update user profile with conditions:
    - fields should not be empty
    - password cannot be updated here
    - same details can't be updated multiple times
    - only logged in user can update
    - return only updated fields
    """
    db = get_db()
    
    # 1. Validate Authorization Header
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization.split(" ")[1]

    # 2. Validate session and get user
    user = await get_user_from_token(token)

    if str(user["_id"]) != str(user_id):
        raise HTTPException(status_code=403, detail="You can only update your own profile")

    # 3. Prevent password updates here
    if "password" in data:
        raise HTTPException(status_code=400, detail="Password can only be updated via Change Password endpoint")

    # 4. Validate non-empty fields
    for field, value in data.items():
        if value is None or (isinstance(value, str) and not value.strip()):
            raise HTTPException(status_code=400, detail=f"{field} cannot be empty")

    # 5. Compare old vs new data
    updates = {}
    for field, value in data.items():
        if field in user and user[field] != value:
            updates[field] = value

    if not updates:
        raise HTTPException(status_code=400, detail="No new changes provided")

    # 6. Apply update
    await db.users.update_one(
        {"_id": ObjectId(user["_id"])},
        {"$set": updates}
    )

    return {
        "status": "success",
        "message": "Profile updated successfully",
        "updated_fields": updates
    }



async def get_profile(user_id: str) -> dict:
    db = get_db()
    user = await db[USERS_COLL].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="Account is inactive or blocked")

    veh = user.get("vehicle_details")
    return {
        "user_id": str(user["_id"]),
        "full_name": user.get("username"),
        "email": user.get("email"),
        "phone_number": user.get("phone"),
        "vehicle_details": veh or None,
        "created_at": user.get("created_at"),
        "last_login": user.get("last_login"),
        "account_status": "active" if user.get("is_active", True) else "inactive",
    }



async def delete_profile(user_id: str) -> None:
    db = get_db()
    res = await db[USERS_COLL].delete_one({"_id": ObjectId(user_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

async def change_password(user_id: str, old_password: str, new_password: str) -> dict:
    db = get_db()
    from app.utils.validators import validate_password
    validate_password(new_password, strong=True)

    user = await db[USERS_COLL].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(old_password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    await db[USERS_COLL].update_one({"_id": ObjectId(user_id)}, {"$set": {"password_hash": hash_password(new_password)}})

async def forgot_password(email: str) -> None:
    db = get_db()
    user = await db[USERS_COLL].find_one({"email": email.lower()})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = str(uuid.uuid4())
    now = datetime.utcnow()
    await db[USERS_COLL].update_one({"_id": user["_id"]}, {"$set": {"reset_token": token, "reset_token_created_at": now}})

    body = f"""Hello {user.get('username')},
You requested to reset your password. Use the following token to reset it:

Reset Token: {token}

This token is valid for {settings.RESET_TOKEN_TTL_MIN} minutes.
"""
    await send_mail(user["email"], "Password Reset Token", body)

async def reset_password(token: str, new_password: str) -> None:
    db = get_db()
    from app.utils.validators import validate_password
    validate_password(new_password, strong=True)

    user = await db[USERS_COLL].find_one({"reset_token": token})
    if not user:
        raise HTTPException(status_code=404, detail="Invalid or expired reset token")

    created_at = user.get("reset_token_created_at")
    if not created_at or (datetime.utcnow() - created_at) > timedelta(minutes=settings.RESET_TOKEN_TTL_MIN):
        raise HTTPException(status_code=400, detail="Reset token has expired, request a new one")

    await db[USERS_COLL].update_one(
        {"_id": user["_id"]},
        {"$set": {"password_hash": hash_password(new_password)}, "$unset": {"reset_token": "", "reset_token_created_at": ""}},
    )
