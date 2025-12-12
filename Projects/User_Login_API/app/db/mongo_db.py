from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URI
 
client = AsyncIOMotorClient(MONGO_URI)

db = client["user_auth_db"]

# collections
user_collection = db["users"]
login_sessions_collection = db["login_sessions"]
token_blacklist_collection = db["token_blacklist"]