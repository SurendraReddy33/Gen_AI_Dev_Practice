from fastapi import Header, HTTPException, Depends
from app.db.mongo_db import token_blacklist_collection
from app.core.security import decode_access_token
 
async def validate_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
 
    token = authorization.split(" ")[1]
 
    # Check if token is blacklisted
    blacklisted = await token_blacklist_collection.find_one({"token": token})
    if blacklisted:
        raise HTTPException(status_code=401, detail="Token has been revoked. Please login again.")
 
    # Decode token for other use
    payload = decode_access_token(token)
    return payload