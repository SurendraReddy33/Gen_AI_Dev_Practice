import os
import secrets
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")


# MongoDB URI
MONGO_URI = "mongodb+srv://surendrareddygandra3:onTwB6qFMES4HF24@genai-cluster.cb98ycb.mongodb.net/"
 

