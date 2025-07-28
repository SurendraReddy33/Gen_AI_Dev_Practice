from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URI
 
client = AsyncIOMotorClient(MONGO_URI)
db = client["user_auth_db"]
user_collection = db["users"]
# token_blacklist_collection = db["token_blacklist"]