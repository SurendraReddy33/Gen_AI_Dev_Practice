import streamlit as st
import os

from rag_pipeline import (
    load_document,
    split_documents,
    create_vector_store,
    agentic_chat_answer
)

st.set_page_config(page_title="Hybrid Agentic RAG Chat", layout="centered")

st.title("🤖 Hybrid Agentic RAG Chat Assistant")
st.write("Ask anything. The assistant will use the document when possible and reason autonomously when needed.")

# -------------------- SESSION STATE --------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# -------------------- FILE UPLOAD --------------------

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    os.makedirs("data/uploads", exist_ok=True)
    file_path = os.path.join("data/uploads", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Processing document..."):
        docs = load_document(file_path)
        chunks = split_documents(docs)
        st.session_state.vector_store = create_vector_store(chunks)
        st.session_state.chat_history = []

    st.success("Document loaded. Start chatting 👇")

# -------------------- CHAT HISTORY --------------------

for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(msg)

# -------------------- CHAT INPUT --------------------

if st.session_state.vector_store:
    user_input = st.chat_input("Ask a question...")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, sources, mode = agentic_chat_answer(
                    st.session_state.vector_store,
                    user_input
                )
                st.write(answer)
                st.caption(f"🧠 Mode: {mode.capitalize()}")

        st.session_state.chat_history.append(("assistant", answer))

        if sources and mode == "grounded":
            with st.expander("Sources"):
                for i, doc in enumerate(sources, 1):
                    page = doc.metadata.get("page", "N/A")
                    st.markdown(f"**Source {i} (Page {page})**")
                    st.write(doc.page_content[:300] + "...")
