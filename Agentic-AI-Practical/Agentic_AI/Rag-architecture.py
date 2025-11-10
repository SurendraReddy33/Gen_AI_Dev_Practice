from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import fitz  # PDF reader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
import google.generativeai as genai  # Gemini API


# ----------------------------------------------------
# Initialize FastAPI
# ----------------------------------------------------
app = FastAPI(title="📘 PDF RAG System (FAISS + Gemini)")

# ----------------------------------------------------
# Load Embedding Model
# ----------------------------------------------------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(MODEL_NAME)

# ----------------------------------------------------
# Gemini Configuration  
# ----------------------------------------------------
api_key = os.getenv("llm-api-key")  # ✅ ensure you set: setx llm_api_key "YOUR_KEY"
if not api_key:
    raise ValueError("❌ Gemini API key not found. Set it using environment variable 'llm_api_key'.")

genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")  # ✅ fast + efficient

# ----------------------------------------------------
# PDF Path
# ----------------------------------------------------
PDF_PATH = "GenAI_Assignment_LangGraph_MultiAgent.pdf"

# ----------------------------------------------------
# Global Storage
# ----------------------------------------------------
chunks_list = []
faiss_index = None

# ----------------------------------------------------
# Helper: Extract Text from PDF
# ----------------------------------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text("text") + "\n"
    return text.strip()

# ----------------------------------------------------
# Request Models
# ----------------------------------------------------
class ChunkRequest(BaseModel):
    chunk_size: Optional[int] = 500
    chunk_overlap: Optional[int] = 100

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


# ----------------------------------------------------
# 1️⃣ Chunk PDF
# ----------------------------------------------------
@app.post("/chunk-pdf")
def chunk_pdf(request: ChunkRequest):
    full_text = extract_text_from_pdf(PDF_PATH)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_text(full_text)

    return {
        "pdf_path": PDF_PATH,
        "num_chunks": len(chunks),
        "chunks_preview": chunks[:3]
    }


# ----------------------------------------------------
# 2️⃣ Embed Chunks
# ----------------------------------------------------
@app.post("/embed-chunks")
def embed_chunks(request: ChunkRequest):
    text = extract_text_from_pdf(PDF_PATH)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap
    )
    chunks = splitter.split_text(text)
    embeddings = embedding_model.encode(chunks)

    return {
        "model_used": MODEL_NAME,
        "num_chunks": len(chunks),
        "embedding_dim": len(embeddings[0]),
        "chunk_sample": chunks[:2],
        "embedding_sample": embeddings[0][:10].tolist()
    }


# ----------------------------------------------------
# 3️⃣ Build FAISS Index
# ----------------------------------------------------
@app.post("/build-index")
def build_index(request: ChunkRequest):
    global chunks_list, faiss_index

    text = extract_text_from_pdf(PDF_PATH)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap
    )
    chunks_list = splitter.split_text(text)

    embeddings = embedding_model.encode(chunks_list).astype("float32")
    embedding_dim = embeddings.shape[1]

    faiss_index = faiss.IndexFlatL2(embedding_dim)
    faiss_index.add(embeddings)

    return {
        "message": "✅ FAISS index built successfully!",
        "num_chunks": len(chunks_list),
        "embedding_dim": embedding_dim
    }


# ----------------------------------------------------
# 4️⃣ Query FAISS
# ----------------------------------------------------
@app.post("/query")
def query_faiss(request: QueryRequest):
    global faiss_index, chunks_list

    if faiss_index is None or len(chunks_list) == 0:
        return {"error": "⚠️ Build FAISS index first using /build-index."}

    query_embedding = embedding_model.encode([request.query]).astype("float32")
    distances, indices = faiss_index.search(query_embedding, request.top_k)

    results = []
    for rank, idx in enumerate(indices[0]):
        if idx < len(chunks_list):
            results.append({
                "rank": rank + 1,
                "chunk": chunks_list[idx],
                "distance": round(float(distances[0][rank]), 4)
            })

    return {
        "query": request.query,
        "top_k": request.top_k,
        "results": results
    }


# ----------------------------------------------------
# 5️⃣ RAG Answer Endpoint (Retrieve + Generate)
# ----------------------------------------------------
@app.post("/rag-answer")
def rag_answer(request: QueryRequest):
    """
    Retrieves top relevant chunks and generates an answer using Gemini.
    Example JSON:
    { "query": "Explain LangGraph and its purpose", "top_k": 3 }
    """
    global faiss_index, chunks_list

    if faiss_index is None or len(chunks_list) == 0:
        return {"error": "⚠️ Build FAISS index first using /build-index."}

    # Step 1: Retrieve top relevant chunks
    query_embedding = embedding_model.encode([request.query]).astype("float32")
    distances, indices = faiss_index.search(query_embedding, request.top_k)
    retrieved_chunks = [chunks_list[i] for i in indices[0] if i < len(chunks_list)]
    context = "\n".join(retrieved_chunks)

    # Step 2: Construct Prompt
    prompt = f"""
    You are an intelligent assistant.
    Based on the following document context, answer the user's query concisely and clearly.

    📘 Context:
    {context}

    💬 Query:
    {request.query}

    ✍️ Answer:
    """

    # Step 3: Generate response using Gemini
    try:
        response = gemini_model.generate_content(prompt)
        answer = response.text.strip()
    except Exception as e:
        answer = f"⚠️ Error generating answer: {str(e)}"

    return {
        "query": request.query,
        "top_k": request.top_k,
        "retrieved_chunks": retrieved_chunks,
        "final_answer": answer
    }