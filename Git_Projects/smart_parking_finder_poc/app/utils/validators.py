
import re
from email_validator import validate_email as _validate_email, EmailNotValidError
from fastapi import HTTPException

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
