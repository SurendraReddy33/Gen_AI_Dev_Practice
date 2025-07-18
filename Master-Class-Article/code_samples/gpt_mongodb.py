from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient # type: ignore
from pydantic import BaseModel
from bson import ObjectId
import bson
 
app = FastAPI()
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.testdb
collection = db.users
 
class User(BaseModel):
    name: str
    age: int
 
@app.post("/users/")
async def create_user(user: User):
    result = await collection.insert_one(user.dict())
    return {"id": str(result.inserted_id)}
 
@app.get("/users/")
async def get_users():
    users = []
    async for doc in collection.find():
        doc["_id"] = str(doc["_id"])
        users.append(doc)
    return users
 
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    raise HTTPException(status_code=404, detail="User not found")
 