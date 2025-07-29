# import secrets
 
# # Generate a secure random secret key (once, then use it)
# SECRET_KEY = secrets.token_hex(32)


# MONGO_URI = "mongodb+srv://surendrareddygandra3:onTwB6qFMES4HF24@genai-cluster.cb98ycb.mongodb.net/"

import os
from dotenv import load_dotenv
 
load_dotenv()  # This will load variables from a `.env` file
 
# Use a fixed secret key for JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-static-secret-key")  # fallback if .env missing
 
# MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://surendrareddygandra3:onTwB6qFMES4HF24@genai-cluster.cb98ycb.mongodb.net/")
 

