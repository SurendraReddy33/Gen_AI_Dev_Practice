from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URI
 
client = AsyncIOMotorClient(MONGO_URI)
db = client["smart_parking_db"]
user_collection = db["users"]
login_sessions_collection = db["login_sessions"]
token_blacklist_collection = db["token_blacklist"]
parkings_collection = db["parking_lots"]
slots_collection = db["slots"]
bookings_collection = db["bookings"]
notifications_collection = db["notifications"]
