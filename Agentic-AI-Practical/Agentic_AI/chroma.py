from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import chromadb

# ----------------------------------------------------
# Initialize FastAPI
# ----------------------------------------------------
app = FastAPI(title="📘 Chroma RAG API (Fixed PDF Path)")

# ----------------------------------------------------
# ChromaDB Client (persistent storage)
# ----------------------------------------------------
chroma_client = chromadb.PersistentClient(path="chroma_store")
collection = chroma_client.get_or_create_collection(name="pdf_chunks")

# ----------------------------------------------------
# Embedding Model
# ----------------------------------------------------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(MODEL_NAME)

# ----------------------------------------------------
# PDF Path (fixed path)
# ----------------------------------------------------
PDF_PATH = "GenAI_Assignment_LangGraph_MultiAgent.pdf"

# ----------------------------------------------------
# Request Models
# ----------------------------------------------------
class ChunkRequest(BaseModel):
    chunk_size: Optional[int] = 500
    chunk_overlap: Optional[int] = 100

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3


# ----------------------------------------------------
# 1️⃣ Build Chroma Index (chunk + embed + store)
# ----------------------------------------------------
@app.post("/build-chroma")
def build_chroma(request: ChunkRequest):
    """
    Loads the fixed PDF, splits it into chunks, generates embeddings,
    and stores them in ChromaDB.
    Example: { "chunk_size": 500, "chunk_overlap": 100 }
    """
    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()

    # Extract full text
    full_text = "\n".join([page.page_content for page in pages])

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap
    )
    chunks = splitter.split_text(full_text)

    # Generate embeddings
    embeddings = embedding_model.encode(chunks).tolist()

    # Store in Chroma collection
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[f"chunk_{i}"],
            documents=[chunk],
            embeddings=[emb]
        )

    return {
        "message": "✅ PDF chunks embedded and stored in ChromaDB successfully!",
        "pdf_path": PDF_PATH,
        "num_chunks": len(chunks)
    }


# ----------------------------------------------------
# 2️⃣ Query Chroma for Similar Chunks
# ----------------------------------------------------
@app.post("/query-chroma")
def query_chroma(request: QueryRequest):
    """
    Searches for top similar chunks in ChromaDB.
    Example: { "query": "What is LangGraph?", "top_k": 3 }
    """
    query_embedding = embedding_model.encode([request.query]).tolist()

    # Search similar chunks
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=request.top_k
    )

    return {
        "query": request.query,
        "top_k": request.top_k,
        "results": [
            {
                "document": doc,
                "distance": round(float(dist), 4)
            }
            for doc, dist in zip(results["documents"][0], results["distances"][0])
        ]
    }

