from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import numpy as np
import faiss
import fitz  # PyMuPDF for PDF reading
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


# Initialize FastAPI
app = FastAPI(title="📘 PDF Chunking API")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(MODEL_NAME)

# PDF Path (change this to your file path
PDF_PATH = "GenAI_Assignment_LangGraph_MultiAgent.pdf"

# Global variables for chunks and FAISS index
chunks_list = []
faiss_index = None


# Function to extract PDF text
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text("text") + "\n"
    return text.strip()


# Define the Request Model (for optional params)
class ChunkRequest(BaseModel):
    chunk_size: Optional[int] = 500       # default chunk size
    chunk_overlap: Optional[int] = 100    # overlap between chunks

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


# Chunking Endpoint
@app.post("/chunk-pdf")
def chunk_pdf(request: ChunkRequest):
    """
    Splits the PDF content into chunks with overlap.
    Send JSON like: { "chunk_size": 500, "chunk_overlap": 100 }
    """

    # 1️⃣ Extract text
    full_text = extract_text_from_pdf(PDF_PATH)

    # 2️⃣ Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_text(full_text)

    # 3️⃣ Return response
    return {
        "pdf_path": PDF_PATH,
        "total_length": len(full_text),
        "chunk_size": request.chunk_size,
        "chunk_overlap": request.chunk_overlap,
        "num_chunks": len(chunks),
        "chunks": chunks[:5]  # returning only first 5 chunks for preview
    }


# Embed the chunks
@app.post("/embed-chunks")
def embed_chunks(request: ChunkRequest):
    """
    Splits the PDF into chunks and generates embeddings for each.
    Example JSON: { "chunk_size": 500, "chunk_overlap": 100 }
    """

    # Extract and split PDF text
    text = extract_text_from_pdf(PDF_PATH)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_text(text)

    # Generate embeddings for all chunks
    embeddings = embedding_model.encode(chunks)

    # Return embeddings info
    return {
        "model_used": MODEL_NAME,
        "pdf_path": PDF_PATH,
        "num_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]) if len(embeddings) > 0 else 0,
        "chunk_preview": chunks[:2],
        "embedding_sample_first_chunk": embeddings[0][:10].tolist() if len(embeddings) > 0 else [],
    }


# 3️⃣ Endpoint: Build FAISS Index
@app.post("/build-index")
def build_faiss_index(request: ChunkRequest):
    """
    Splits the PDF into chunks, embeds them, and stores embeddings in FAISS.
    """

    global chunks_list, faiss_index

    # Extract text and split into chunks
    text = extract_text_from_pdf(PDF_PATH)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks_list = splitter.split_text(text)

    # Generate embeddings
    embeddings = embedding_model.encode(chunks_list)
    embeddings = np.array(embeddings).astype("float32")

    # Create FAISS index
    embedding_dim = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(embedding_dim)
    faiss_index.add(embeddings)

    return {
        "message": "✅ FAISS index built successfully!",
        "model_used": MODEL_NAME,
        "pdf_path": PDF_PATH,
        "num_chunks": len(chunks_list),
        "embedding_dimension": embedding_dim
    }


# 4️⃣ Endpoint: Query the FAISS Index
@app.post("/query")
def query_faiss(request: QueryRequest):
    """
    Search for most similar chunks for a given query.
    Example JSON: { "query": "Explain LangGraph", "top_k": 3 }
    """

    global faiss_index, chunks_list

    if faiss_index is None or len(chunks_list) == 0:
        return {"error": "⚠️ Build FAISS index first using /build-index."}

    # Embed the query
    query_embedding = embedding_model.encode([request.query]).astype("float32")

    # Search top-k similar chunks
    distances, indices = faiss_index.search(query_embedding, request.top_k)

    # Prepare response
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
        "num_results": len(results),
        "results": results
    }