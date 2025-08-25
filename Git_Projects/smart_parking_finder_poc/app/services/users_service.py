
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from bson import ObjectId
import uuid

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

    await db[USERS_COLL].update_one({"_id": user["_id"]}, {"$set": {"last_login": datetime.utcnow()}})

    token = generate_jwt(str(user["_id"]), user.get("role", "user"))
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

async def update_profile(user_id: str, updates: dict) -> None:
    db = get_db()
    allowed = {k: v for k, v in updates.items() if k in {"username", "email", "phone"} and v is not None}
    if not allowed:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    # validations & uniqueness
    if "email" in allowed:
        validate_email(allowed["email"])
        exists = await db[USERS_COLL].find_one({"email": allowed["email"].lower(), "_id": {"$ne": ObjectId(user_id)}})
        if exists:
            raise HTTPException(status_code=400, detail="Email already exists")
        allowed["email"] = allowed["email"].lower()
    if "username" in allowed:
        exists = await db[USERS_COLL].find_one({"username": allowed["username"], "_id": {"$ne": ObjectId(user_id)}})
        if exists:
            raise HTTPException(status_code=400, detail="Username already exists")
    if "phone" in allowed:
        from app.utils.validators import validate_phone
        validate_phone(allowed["phone"])

    res = await db[USERS_COLL].update_one({"_id": ObjectId(user_id)}, {"$set": allowed})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

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
