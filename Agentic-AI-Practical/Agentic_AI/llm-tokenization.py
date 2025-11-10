from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
import numpy as np

# ✅ Initialize FastAPI
app = FastAPI(title="Hugging Face Tokenizer API")

# ✅ Load model and tokenizer properly
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# ✅ Define request model
class TextRequest(BaseModel):
    text: str
    text2: Optional[str] = None
    sentences: Optional[list[str]] = None
    top_k: Optional[int] = 3



# ✅ Tokenization endpoint
@app.post("/tokenize")
def tokenize_text(request: TextRequest):
    text = request.text

    # --- Tokenize ---
    tokens = tokenizer.tokenize(text)                # list of tokens (strings)
    token_ids = tokenizer.encode(text)               # numerical IDs
    token_count = len(token_ids)                     # count

    # --- Return result ---
    return {
        "model": MODEL_NAME,
        "text": text,
        "tokens": tokens,
        "token_ids": token_ids,
        "token_count": token_count
    }


# Embedding endpoint
@app.post("/embeddings")
def generate_embedding(request: TextRequest):
    text = request.text

    # Generate embeddings using SentenceTransformer
    embedding = embedding_model.encode(text)

    # Convert safely to list
    if not isinstance(embedding, list):
        embedding = embedding.tolist()

    return {
        "model_name": MODEL_NAME,
        "text": text,
        "embedding_length": len(embedding),
        "embedding_sample": embedding[:10]  # first 10 numbers only
    }


# Cosine similarity endpoint
@app.post("/cosine-similarity")
def cosine_similarity(request: TextRequest):
    """
    Computes cosine similarity between two sentences.
    """
    # Generate embeddings
    emb1 = embedding_model.encode(request.text)
    emb2 = embedding_model.encode(request.text2)

    # Compute cosine similarity
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    return {
        "model_name": MODEL_NAME,
        "text1": request.text,
        "text2": request.text2,
        "similarity_score": round(float(similarity), 3)
    }


# ✅ Finding most similar sentences endpoint
@app.post("/find-similar")
def find_most_similar(request: TextRequest):
    query = request.text                    # ✅ fixed field name
    sentences = request.sentences or []     # ✅ safety check
    if not sentences:
        return {"error": "Please provide a list of sentences to compare against."}

    top_k = min(request.top_k or 3, len(sentences))

    # Encode sentences and query
    sentence_embeddings = embedding_model.encode(sentences)
    query_embedding = embedding_model.encode(query)

    # Compute cosine similarities
    similarities = np.dot(sentence_embeddings, query_embedding) / (
        np.linalg.norm(sentence_embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    # Sort and get top-k
    sorted_indices = np.argsort(similarities)[::-1]
    results = [
        {"sentence": sentences[i], "similarity_score": round(float(similarities[i]), 3)}
        for i in sorted_indices[:top_k]
    ]

    return {
        "model_name": MODEL_NAME,
        "query": query,
        "top_results": results
    }


