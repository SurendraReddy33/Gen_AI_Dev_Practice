from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# -------------------- HELPERS --------------------

def normalize_text(text):
    replacements = {
        "PROJECTS": "Projects",
        "SKILLS": "Skills",
        "EXPERIENCE": "Experience",
        "CERTIFICATIONS": "Certifications"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def add_section_hints(text):
    sections = ["Projects", "Skills", "Experience", "Certifications"]
    for sec in sections:
        text = text.replace(sec, f"\n\nSECTION: {sec}\n")
    return text


def get_dynamic_k(chunks_len):
    if chunks_len <= 10:
        return 5
    elif chunks_len <= 30:
        return 7
    return 10


def filter_short_chunks(docs, min_len=100):
    return [doc for doc in docs if len(doc.page_content) >= min_len]

# -------------------- STEP 1: LOAD --------------------

def load_document(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()

# -------------------- STEP 2: SPLIT --------------------

def split_documents(documents):
    for doc in documents:
        doc.page_content = add_section_hints(doc.page_content)
        doc.page_content = normalize_text(doc.page_content)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=60
    )
    return splitter.split_documents(documents)

# -------------------- STEP 3: VECTOR STORE --------------------

def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    return FAISS.from_documents(chunks, embeddings)

# -------------------- STEP 4: RAG CHAIN --------------------

def create_rag_chain(vector_store, chunks_len):
    k = get_dynamic_k(chunks_len)
    retriever = vector_store.as_retriever(search_kwargs={"k": k})

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )

    prompt = PromptTemplate.from_template(
        """
You are answering questions from a document such as a resume.

Rules:
- Use ONLY the given context
- Be concise and factual
- If multiple items exist, list them clearly
- If information is missing, say:
"Answer not available in the provided document."

Context:
{context}

Question:
{question}

Answer (use bullet points if applicable):
"""
    )

    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    return rag_chain

# -------------------- STEP 5: RETRIEVAL WITH SOURCES --------------------

def retrieve_with_sources(vector_store, question, chunks_len):
    k = get_dynamic_k(chunks_len)
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(question)
    return filter_short_chunks(docs)

# -------------------- OPTIONAL TEST --------------------

if __name__ == "__main__":
    pdf_path = r"data\Surendra_Reddy_Agentic_AI_Developer.pdf"

    docs = load_document(pdf_path)
    chunks = split_documents(docs)

    vector_store = create_vector_store(chunks)
    rag_chain = create_rag_chain(vector_store, len(chunks))

    q = "List all projects mentioned"
    response = rag_chain.invoke(q)

    print(response.content)
