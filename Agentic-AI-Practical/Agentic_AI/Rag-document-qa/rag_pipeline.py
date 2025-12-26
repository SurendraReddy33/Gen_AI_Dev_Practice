from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# -------------------- STEP 1: LOAD & SPLIT --------------------

def load_document(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=60
    )
    chunks = splitter.split_documents(documents)

    # Normalize headings for better retrieval
    for chunk in chunks:
        chunk.page_content = normalize_text(chunk.page_content)

    return chunks

def normalize_text(text):
    replacements = {
        "PROJECTS": "Projects",
        "SKILLS": "Skills",
        "EXPERIENCE": "Experience"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# -------------------- STEP 2: EMBEDDINGS + FAISS --------------------

def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    return FAISS.from_documents(chunks, embeddings)


# -------------------- STEP 3: RAG (MODERN, STABLE) --------------------

def create_rag_chain(vector_store):
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )

    prompt = PromptTemplate.from_template(
        """
You are a helpful assistant.
Answer ONLY using the context below.
If the answer is not present, say:
"Answer not available in the provided document."

Context:
{context}

Question:
{question}

Answer:
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


def retrieve_with_sources(vector_store, question, k=5):
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(question)
    return docs


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)




# -------------------- TEST FULL RAG --------------------

if __name__ == "__main__":
    pdf_path = "data/Surendra_Reddy_Agentic_AI_Developer.pdf"

    docs = load_document(pdf_path)
    chunks = split_documents(docs)
    print(f"Total chunks: {len(chunks)}")

    vector_store = create_vector_store(chunks)
    print("Vector store ready.")

    rag_chain = create_rag_chain(vector_store)

    question = "What projects has the candidate worked on?"
    response = rag_chain.invoke(question)

    print("Answer:\n", response.content)
