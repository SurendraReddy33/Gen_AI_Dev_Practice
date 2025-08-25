from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

mongodb = MongoDB()

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)
    mongodb.database = mongodb.client[settings.DATABASE_NAME]
    print(f"Connected to MongoDB: {settings.MONGODB_URL}")

async def close_mongo_connection():
    if mongodb.client:
        mongodb.client.close()
        print("Closed MongoDB connection")

def get_database():
    return mongodb.database
