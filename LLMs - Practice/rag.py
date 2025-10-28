import os
import uuid
import gradio as gr
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import SQLChatMessageHistory
from sqlalchemy import create_engine
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
import tempfile
from fastapi import FastAPI , HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware



os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


app= FastAPI(title=".PDF based chatbot")


# CORS (optional, useful for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#  Setup LLM + Embeddings

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


#  Globals

# Maintain per-session state keyed by session_id
vector_store_by_session = {}
conversation_chain_by_session = {}
last_uploaded_file_by_session = {}

def get_database_url():
    # e.g., postgresql+psycopg2://postgres:postgres@localhost:5432/rag_chat
    return os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/rag_chat")

# Create a single SQLAlchemy engine for chat history
db_engine = create_engine(get_database_url())

def build_memory_for_session(session_id: str) -> ConversationBufferMemory:
    chat_history = SQLChatMessageHistory(
        connection=db_engine,
        session_id=session_id,
        table_name=os.getenv("CHAT_HISTORY_TABLE", "langchain_chat_history")
    )
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        chat_memory=chat_history,
        input_key="question",
        output_key="answer"
    )

CUSTOM_PROMPT = """You are a helpful assistant. Use the following context to answer the question.
If the answer is not contained in the context, respond exactly with:
"I don't know, it is not related to the PDF."

Context:
{context}

Question:
{question}

Answer:"""


# -----------------------
# 📄 PDF Loading & Processing
# -----------------------
def load_pdf(file, session_id: str):
    global vector_store_by_session, conversation_chain_by_session, last_uploaded_file_by_session

    if file is None:
        return " No file uploaded."

    #file_path = file.name

    # If file is a string (filepath), just use it directly
    if isinstance(file, str):
        file_path = file

    else:
        # file is file-like object: save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            file_path = tmp.name

    # filename = os.path.basename(file.name)
    # # Save the uploaded file to a temporary path
    # file_path = f"temp_{filename}"
    # with open(file_path, "wb") as f:
    #     f.write(file.read())  # Save uploaded file contents

    loader = PyPDFLoader(file_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    docs = splitter.split_documents(pages)

    # Use FAISS in-memory vector store for speed (per session)
    vector_store = FAISS.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever()

    prompt_template = PromptTemplate(
        template=CUSTOM_PROMPT,
        input_variables=["context", "question"]
    )

    # Reuse existing memory for this session; create if not present
    existing_chain = conversation_chain_by_session.get(session_id)
    memory = existing_chain.memory if existing_chain is not None else build_memory_for_session(session_id)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt_template},
        return_source_documents=True
    )
    vector_store_by_session[session_id] = vector_store
    conversation_chain_by_session[session_id] = conversation_chain
    last_uploaded_file_by_session[session_id] = getattr(file, 'name', file)

    return " PDF loaded and processed successfully!"



# Query Handler

def handle_query(query, session_id: str):
    if not query.strip():
        return " Please ask a valid question."

    if any(word in query.lower() for word in ["exit", "quit", "bye", "goodbye"]):
        return "Thanks! Goodbye "

    conversation_chain = conversation_chain_by_session.get(session_id)
    if conversation_chain is None:
        return " Please upload and process a PDF first."

    try:
        # Early small-talk fallback (avoid RAG when it's clearly chit-chat)
        small_talk_terms = [
            "thanks", "thank you", "thank u", "great thank you", "great thanks",
            "ok", "okay", "k", "cool", "nice", "awesome",
            "hello", "hi", "hey", "yo", "good morning", "good evening", "good night",
            "bye", "goodbye", "see you", "take care",
            "how are you", "who are you", "help",
        ]
        ql = query.strip().lower()
        word_count = len([w for w in ql.split() if w.isalpha()])
        if any(term in ql for term in small_talk_terms) or (word_count <= 3 and not ql.endswith("?")):
            fallback = llm.invoke([HumanMessage(content=query)])
            return fallback.content

        result = conversation_chain.invoke({"question": query})
        answer = result.get("answer", "")
        sources = result.get("source_documents", []) or []
        if not sources:
            return "I don't know, it is not related to the PDF."
        return answer
    except Exception as e:
        return f" Error during query: {e}"


# Process User Interaction

def process_and_respond(message, history, file, session_id):
    global last_uploaded_file_by_session

    status_msg = ""

    # Initialize session id if missing
    if not session_id:
        session_id = str(uuid.uuid4())

    # Load new PDF if different from previous for this session
    last_uploaded_file = last_uploaded_file_by_session.get(session_id)
    if file is not None and (last_uploaded_file != file.name):
        status_msg = load_pdf(file, session_id)
        history = []

    # If no message
    if not message.strip():
        return history + [[message, " Please enter a valid question."]], status_msg or " No input."

    # Get bot response
    response = handle_query(message, session_id)

    # Update history
    history.append([message, response])
    return history, status_msg



#  Gradio UI


with gr.Blocks() as demo:
    gr.Markdown("## 🤖 PDF Chatbot (Gemini + RAG)")

    with gr.Row():
        with gr.Column(scale=3):
            file_input = gr.File(label="📎 Upload PDF", file_types=[".pdf"])
        with gr.Column(scale=7):
            status_output = gr.Textbox(label="📂 Status", interactive=False)

    chatbot = gr.Chatbot(label="🗨️ Chat with your PDF", elem_id="chatbot")
    session_id_box = gr.Textbox(label="🔑 Session ID", value=str(uuid.uuid4()), info="Keep this constant to resume memory.")
    user_msg = gr.Textbox(placeholder="Type your question and press Enter...", label="💬 Your Message", lines=1)

    # Main interaction function
    user_msg.submit(
        fn=process_and_respond,
        inputs=[user_msg, chatbot, file_input, session_id_box],
        outputs=[chatbot, status_output]
    ).then(lambda: "", None, user_msg)  # Clear input after submit


#  Mount Gradio app into FastAPI
gradio_app = gr.mount_gradio_app(app, demo, path="/chat")

# Optional: add endpoint to return Gradio URL
@app.get("/start_chatbot_application")
def chatbot_application():
    return JSONResponse(
        content={"message": "Chatbot is running", "url": "http://localhost:8000/chat"},
        status_code=200
    )
