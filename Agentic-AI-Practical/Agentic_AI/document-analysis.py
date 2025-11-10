from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
import numpy as np
import fitz  # PyMuPDF for PDF text extraction

# ----------------------------------------------------
# Initialize FastAPI
# ----------------------------------------------------
app = FastAPI(title="📘 Local PDF Semantic Analyzer (JSON Input)")

# ----------------------------------------------------
# Load Model and Tokenizer
# ----------------------------------------------------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# ----------------------------------------------------
# Define Request Model (for JSON body)
# ----------------------------------------------------
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

# ----------------------------------------------------
# Path to Local PDF
# ----------------------------------------------------
PDF_PATH = "GenAI_Assignment_LangGraph_MultiAgent.pdf"  # 👈 Change this to your PDF path

# ----------------------------------------------------
# Extract text from PDF
# ----------------------------------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    """Read and extract text from a local PDF file."""
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text("text") + "\n"
    return text.strip()

# ----------------------------------------------------
# Load PDF text and precompute embeddings (for speed)
# ----------------------------------------------------
DOCUMENT_TEXT = extract_text_from_pdf(PDF_PATH)
SENTENCES = [line.strip() for line in DOCUMENT_TEXT.split("\n") if line.strip()]
SENTENCE_EMBEDDINGS = model.encode(SENTENCES)

# ----------------------------------------------------
# Main Endpoint: Query local PDF using JSON input
# ----------------------------------------------------
@app.post("/query-pdf")
async def query_pdf_json(request: QueryRequest):
    """
    Send a JSON body with 'query' and 'top_k'.
    The system reads the PDF locally and returns top-k similar sentences.
    """

    query = request.query
    top_k = request.top_k

    # 🧠 Step 1: Tokenize query
    query_tokens = tokenizer.tokenize(query)

    # 🔢 Step 2: Generate embedding for query
    query_embedding = model.encode(query)

    # 🔍 Step 3: Compute cosine similarity
    similarities = np.dot(SENTENCE_EMBEDDINGS, query_embedding) / (
        np.linalg.norm(SENTENCE_EMBEDDINGS, axis=1) * np.linalg.norm(query_embedding)
    )

    # 📊 Step 4: Sort and select top-k
    top_k = min(top_k, len(SENTENCES))
    sorted_indices = np.argsort(similarities)[::-1]

    top_results = [
        {
            "sentence": SENTENCES[i],
            "similarity_score": round(float(similarities[i]), 3)
        }
        for i in sorted_indices[:top_k]
    ]

    # 🚀 Step 5: Return final response
    return {
        "model_used": MODEL_NAME,
        "pdf_path": PDF_PATH,
        "query": query,
        "query_tokens": query_tokens,
        "total_sentences": len(SENTENCES),
        "top_k": top_k,
        "top_results": top_results
    }