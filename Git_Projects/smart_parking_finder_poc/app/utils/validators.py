
from datetime import datetime, timedelta
import re
from email_validator import validate_email as _validate_email, EmailNotValidError
from fastapi import HTTPException

from app.config.db import get_db

SESSION_EXP_TIME = 60

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_IN_RE = re.compile(r"^[6-9]\d{9}$")  # simple India 10-digit starting 6-9
PASSWORD_RE = re.compile(r"^.{6,}$")

def validate_email(email: str) -> None:
    try:
        _validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail="Invalid email format")

def validate_phone(phone: str) -> None:
    if not PHONE_IN_RE.match(phone or ""):
        raise HTTPException(status_code=400, detail="Invalid phone number")

def validate_password(password: str, strong: bool = False) -> None:
    if not PASSWORD_RE.match(password or ""):
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    if strong:
        # must include uppercase, lowercase, number, special char
        if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password) or not re.search(r"[^A-Za-z0-9]", password):
            raise HTTPException(status_code=400, detail="New password must be at least 6 characters long and include uppercase, lowercase, number, and special character")
        

async def store_session(email: str, username: str, token: str):
    db = get_db()
    # Remove any old sessions beyond expiry duration
    await db.login_sessions.delete_many({
        "email": email,
        "created_at": {
            "$lt": datetime.utcnow() - timedelta(minutes=SESSION_EXP_TIME)
        }
    })
    # Check if an active session already exists
    existing = await db.login_sessions.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=410, detail="Active session exists. Please logout or wait till it expires.")
    
    session_doc = {
        "email": email,
        "username": username,
        "token": token,
        "created_at": datetime.utcnow(),
        "status": "Active"
    }
    await db.login_sessions.insert_one(session_doc)
 