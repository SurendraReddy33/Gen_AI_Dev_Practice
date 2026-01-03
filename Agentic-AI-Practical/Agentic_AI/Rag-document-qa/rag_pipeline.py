import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

# -------------------- LOAD DOCUMENT --------------------

def load_document(path):
    return PyPDFLoader(path).load()

# -------------------- SPLIT DOCUMENT --------------------

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=80
    )
    return splitter.split_documents(docs)

# -------------------- VECTOR STORE --------------------

def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    if os.path.exists("faiss_index"):
        return FAISS.load_local(
            "faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )

    vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local("faiss_index")
    return vs

# -------------------- RETRIEVAL --------------------

def retrieve_sources(vector_store, question):
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 10}
    )
    return retriever.invoke(question)

# -------------------- STRICT GROUNDED ANSWER --------------------

def grounded_answer(sources, question, chat_history):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1
    )

    conversation = "\n".join(
        f"{role}: {msg}" for role, msg in chat_history[-6:]
    )

    prompt = PromptTemplate.from_template(
        """
You are a document question-answering assistant.

RULES (VERY IMPORTANT):
- Answer ONLY using the document context
- Do NOT add external knowledge
- Do NOT assume or guess
- If partial information exists, answer partially
- If information does not exist, clearly say so
- Use bullet points when listing items
- Be precise and factual

Conversation (for reference only):
{conversation}

Document Context:
{context}

Question:
{question}

Accurate Answer:
"""
    )

    context_text = "\n\n".join(doc.page_content for doc in sources)

    response = llm.invoke(
        prompt.format(
            conversation=conversation,
            context=context_text,
            question=question
        )
    )

    return response.content

# -------------------- MAIN ENTRY --------------------

def document_chat_answer(vector_store, question, chat_history):
    sources = retrieve_sources(vector_store, question)

    if not sources:
        return (
            "The document does not contain information related to this question.",
            [],
        )

    answer = grounded_answer(sources, question, chat_history)
    return answer, sources
