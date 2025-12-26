import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -------------------- STEP 1: LOAD & SPLIT --------------------

def load_document(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80
    )
    chunks = splitter.split_documents(documents)
    return chunks


# -------------------- STEP 2: EMBEDDINGS + FAISS --------------------

def create_vector_store(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store


# -------------------- TESTING STEP 2 --------------------

if __name__ == "__main__":
    pdf_path = r"data\Surendra_Reddy_Agentic_AI_Developer.pdf"

    docs = load_document(pdf_path)
    chunks = split_documents(docs)

    print(f"Total chunks: {len(chunks)}")

    vector_store = create_vector_store(chunks)
    print("FAISS vector store created successfully.")

    # Test retrieval
    query = "What is this document about?"
    results = vector_store.similarity_search(query, k=3)

    print("\nTop matching chunks:")
    for i, doc in enumerate(results, 1):
        print(f"\nResult {i}:\n{doc.page_content[:300]}")
