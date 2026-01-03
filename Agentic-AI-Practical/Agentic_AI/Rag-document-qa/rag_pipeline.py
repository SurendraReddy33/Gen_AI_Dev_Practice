import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# -------------------- HELPERS --------------------

def normalize_text(text):
    for k in ["PROJECTS", "SKILLS", "EXPERIENCE", "CERTIFICATIONS"]:
        text = text.replace(k, k.title())
    return text


def add_section_hints(text):
    for sec in ["Projects", "Skills", "Experience", "Certifications"]:
        text = text.replace(sec, f"\n\nSECTION: {sec}\n")
    return text


def get_dynamic_k(n):
    return 5 if n <= 10 else 7 if n <= 30 else 10


def deduplicate_lines(text):
    seen, out = set(), []
    for line in text.split("\n"):
        l = line.strip()
        if l and l.lower() not in seen:
            seen.add(l.lower())
            out.append(l)
    return "\n".join(out)

# -------------------- LOAD & SPLIT --------------------

def load_document(path):
    return PyPDFLoader(path).load()


def split_documents(docs):
    for d in docs:
        d.page_content = normalize_text(add_section_hints(d.page_content))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=60
    )
    return splitter.split_documents(docs)

# -------------------- VECTOR STORE --------------------

def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if os.path.exists("faiss_index"):
        return FAISS.load_local(
            "faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )

    vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local("faiss_index")
    return vs

# -------------------- AGENT 1: PLANNER --------------------

def planner_agent(question):
    q = question.lower()
    if "project" in q:
        return "Projects"
    if "skill" in q:
        return "Skills"
    if "experience" in q or "work" in q:
        return "Experience"
    if "certification" in q:
        return "Certifications"
    return None

# -------------------- AGENT 2: RETRIEVER --------------------

def retrieve_with_sources(vector_store, question, chunks_len):
    k = get_dynamic_k(chunks_len)
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(question)

    section = planner_agent(question)
    if section:
        docs = [d for d in docs if section.lower() in d.page_content.lower()]

    return docs

# -------------------- AGENT 3: ANSWER GENERATOR --------------------

def create_answer_chain(vector_store, chunks_len):
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.2
    )

    prompt = PromptTemplate.from_template(
        """
You are an AI assistant answering questions from a document.

Rules:
- Use ONLY the given context
- List ALL relevant items
- Use bullet points if applicable
- Do NOT hallucinate
- If missing, say:
"Answer not available in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": get_dynamic_k(chunks_len)}
    )

    return (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

# -------------------- AGENT 4: VERIFIER --------------------

def verifier_agent(answer, sources):
    if "not available" in answer.lower():
        return answer

    for doc in sources:
        if any(word.lower() in doc.page_content.lower() for word in answer.split()):
            return answer

    return "Answer not available in the provided document."

# -------------------- MAIN AGENTIC PIPELINE --------------------

def agentic_rag_answer(vector_store, chunks_len, question):
    sources = retrieve_with_sources(vector_store, question, chunks_len)
    answer_chain = create_answer_chain(vector_store, chunks_len)

    response = answer_chain.invoke(question)
    raw_answer = deduplicate_lines(response.content)

    final_answer = verifier_agent(raw_answer, sources)
    return final_answer, sources
