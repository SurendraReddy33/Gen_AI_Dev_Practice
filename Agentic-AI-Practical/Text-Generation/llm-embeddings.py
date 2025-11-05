from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import numpy as np
import faiss
import os

# ---------- Setup ----------
api_key = os.getenv("llm-api-key")
client = genai.Client(api_key=api_key)

app = FastAPI(title="Embeddings API")

# ---------- In-Memory FAISS Setup ----------
dimension = 500            # embedding vector size
index = faiss.IndexFlatL2(dimension)
texts_db = []               # to map vectors back to text


# ---------- Models ----------
class EmbedRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3


# ---------- 1️⃣ Generate Embeddings ----------
@app.post("/embed/text")
async def generate_embedding(request: EmbedRequest):
    try:
        response = client.models.embed_content(
            model="models/embedding-001",
            contents=request.text
        )
        vector = np.array(response.embedding.values, dtype="float32")
        return {"embedding": vector.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- 2️⃣ Store Text + Embedding ----------
@app.post("/embed/store")
async def store_embedding(request: EmbedRequest):
    response = client.models.embed_content(
        model="models/embedding-001",
        contents=request.text
    )
    vector = np.array(response.embedding.values, dtype="float32")
    index.add(np.array([vector]))
    texts_db.append(request.text)
    return {"message": "Text embedded and stored successfully!"}


# ---------- 3️⃣ Search Semantically ----------
@app.post("/embed/search")
async def search_similar(request: SearchRequest):
    if len(texts_db) == 0:
        raise HTTPException(status_code=404, detail="No data stored yet.")

    query_emb = client.models.embed_content(
        model="models/embedding-001",
        contents=request.query
    )
    query_vec = np.array([query_emb.embedding.values], dtype="float32")

    distances, indices = index.search(query_vec, request.top_k)
    results = [
        {"text": texts_db[i], "distance": float(distances[0][pos])}
        for pos, i in enumerate(indices[0])
    ]

    return {"query": request.query, "results": results}
