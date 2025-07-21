from pymongo import MongoClient
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from sentence_transformers import SentenceTransformer
import torch
 
# Load GPT2
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")
gpt2_model.eval()
 
# Load Sentence Transformer
embedder = SentenceTransformer("all-MiniLM-L6-v2")
 
# MongoDB connection
client = MongoClient("mongodb+srv://surendrareddygandra3:onTwB6qFMES4HF24@genai-cluster.cb98ycb.mongodb.net/")
db = client["Master-class"]
collection = db["Sentence_transformers"]