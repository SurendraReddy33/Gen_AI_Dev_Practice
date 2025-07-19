from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from sentence_transformers import SentenceTransformer
import torch
 
# ------------- INIT ------------- #
app = FastAPI()
 
# MongoDB (change URI if needed)
client = MongoClient("mongodb+srv://surendrareddygandra3:onTwB6qFMES4HF24@genai-cluster.cb98ycb.mongodb.net/")
db = client["Master-class"]
collection = db["Sentence_transformers"]
 
# Load models
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")
gpt2_model.eval()
 
embedder = SentenceTransformer("all-MiniLM-L6-v2")
 
 
# ------------- Schema ------------- #
class PromptInput(BaseModel):
    prompt: str
 
 
# ------------- Routes ------------- #
 
@app.post("/generate_store", tags=["Store Prompt + GPT2 + Embeddings"])
async def generate_and_store(data: PromptInput):
    prompt_text = data.prompt
 
    # Tokenize
    tokens = gpt2_tokenizer.encode(prompt_text, return_tensors="pt")[0].tolist()
    GPT2TOKENIZER = gpt2_tokenizer.tokenize(prompt_text)

    # Generate GPT2 response
    gpt_input = torch.tensor([tokens])
    gpt_output = gpt2_model.generate(gpt_input, max_length=100)
    generated_text = gpt2_tokenizer.decode(gpt_output[0], skip_special_tokens=True)
 
    # Embedding
    embedding = embedder.encode(prompt_text).tolist()
 
    # Save to MongoDB
    doc = {
        "prompt": prompt_text,
        "tokens": [tokens,GPT2TOKENIZER],
        "embedding": embedding,
        "gpt2_response": generated_text,
    }
    collection.insert_one(doc)
 
    return {
        "message": "Stored successfully",
        "prompt": prompt_text,
        "gpt2_response": generated_text
    }
 
 
@app.post("/search_prompt", tags=["Semantic Search"])
async def semantic_search(data: PromptInput):
    query_embed = embedder.encode(data.prompt, convert_to_tensor=True)
    docs = list(collection.find({}, {"_id": 0, "prompt": 1, "gpt2_response": 1, "embedding": 1}))
 
    if not docs:
        return {"message": "No data in database"}
 
    stored_embeddings = torch.tensor([doc["embedding"] for doc in docs])
    similarities = torch.nn.functional.cosine_similarity(query_embed, stored_embeddings)
 
    top_index = torch.argmax(similarities).item()
    match = docs[top_index]
 
    return {
        "closest_prompt": match["prompt"],
        "response": match["gpt2_response"],
        "similarity_score": round(similarities[top_index].item(), 4)
    }
 
 
@app.get("/", tags=["Info"])
def root():
    return {"message": "GPT2 + Embeddings + Tokens + MongoDB + FastAPI"}
 