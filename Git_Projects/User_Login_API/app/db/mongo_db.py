from pymongo import MongoClient
 
MONGO_URI = "mongodb+srv://surendrareddygandra3:onTwB6qFMES4HF24@genai-cluster.cb98ycb.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["user_auth_db"]
user_collection = db["users"]