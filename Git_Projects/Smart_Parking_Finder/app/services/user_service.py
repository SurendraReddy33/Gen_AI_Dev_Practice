from datetime import datetime, timedelta
import uuid
from passlib.context import CryptContext
from app.models.user import UserCreate, UserUpdate
from app.database.mongodb import get_database
from app.utils.validators import validate_password_complexity
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db):
        self.db = db
        self.users_collection = db["users"]
    
    async def get_user_by_email(self, email: str):
        return await self.users_collection.find_one({"email": email})
    
    async def get_user_by_username(self, username: str):
        return await self.users_collection.find_one({"username": username})
    
    async def get_user_by_id(self, user_id: str):
        return await self.users_collection.find_one({"_id": user_id})
    
    async def create_user(self, user: UserCreate):
        hashed_password = pwd_context.hash(user.password)
        user_data = {
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "hashed_password": hashed_password,
            "role": "user",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "last_login": None
        }
        
        result = await self.users_collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        return user_data
    
    async def authenticate_user(self, email: str, password: str):
        user = await self.get_user_by_email(email)
        if not user:
            return False
        
        if not pwd_context.verify(password, user["hashed_password"]):
            return False
        
        # Update last login
        await self.users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        return user
    
    async def update_user(self, user_id: str, update_data: UserUpdate):
        update_fields = {}
        
        if update_data.username:
            # Check if username is unique
            existing_user = await self.get_user_by_username(update_data.username)
            if existing_user and existing_user["_id"] != user_id:
                raise ValueError("Username already exists")
            update_fields["username"] = update_data.username
        
        if update_data.email:
            # Check if email is unique
            existing_user = await self.get_user_by_email(update_data.email)
            if existing_user and existing_user["_id"] != user_id:
                raise ValueError("Email already exists")
            update_fields["email"] = update_data.email
        
        if update_data.phone:
            if not re.match(r'^\d{10}$', update_data.phone):
                raise ValueError("Phone must be 10 digits")
            update_fields["phone"] = update_data.phone
        
        if not update_fields:
            return False
        
        result = await self.users_collection.update_one(
            {"_id": user_id},
            {"$set": update_fields}
        )
        
        return result.modified_count > 0
    
    async def delete_user(self, user_id: str):
        result = await self.users_collection.delete_one({"_id": user_id})
        return result.deleted_count > 0
    
    async def change_password(self, user_id: str, old_password: str, new_password: str):
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        if not pwd_context.verify(old_password, user["hashed_password"]):
            return False
        
        validate_password_complexity(new_password)
        
        hashed_password = pwd_context.hash(new_password)
        result = await self.users_collection.update_one(
            {"_id": user_id},
            {"$set": {"hashed_password": hashed_password}}
        )
        
        return result.modified_count > 0
    
    async def generate_reset_token(self, user_id: str):
        reset_token = str(uuid.uuid4())
        reset_token_expires = datetime.utcnow() + timedelta(minutes=30)
        
        await self.users_collection.update_one(
            {"_id": user_id},
            {"$set": {
                "reset_token": reset_token,
                "reset_token_expires": reset_token_expires
            }}
        )
        
        return reset_token
    
    async def reset_password(self, reset_token: str, new_password: str):
        user = await self.users_collection.find_one({
            "reset_token": reset_token,
            "reset_token_expires": {"$gt": datetime.utcnow()}
        })
        
        if not user:
            return False
        
        validate_password_complexity(new_password)
        
        hashed_password = pwd_context.hash(new_password)
        result = await self.users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "hashed_password": hashed_password
            }, "$unset": {
                "reset_token": "",
                "reset_token_expires": ""
            }}
        )
        
        return result.modified_count > 0
