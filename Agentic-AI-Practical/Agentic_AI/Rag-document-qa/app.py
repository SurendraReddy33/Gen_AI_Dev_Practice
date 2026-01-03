import streamlit as st
import os

from rag_pipeline import (
    load_document,
    split_documents,
    create_vector_store,
    create_rag_chain,
    retrieve_with_sources,
    deduplicate_lines
)

st.set_page_config(page_title="Chat with Document (RAG)", layout="centered")

st.title("💬 Chat with Your Document")
st.write("Upload a document and chat with it using RAG.")

# -------------------- SESSION STATE --------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chunks_len" not in st.session_state:
    st.session_state.chunks_len = 0

# -------------------- FILE UPLOAD --------------------

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    os.makedirs("data/uploads", exist_ok=True)
    file_path = os.path.join("data/uploads", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Document uploaded successfully.")

    with st.spinner("Processing document..."):
        docs = load_document(file_path)
        chunks = split_documents(docs)
        vector_store = create_vector_store(chunks)
        rag_chain = create_rag_chain(vector_store, len(chunks))

        st.session_state.vector_store = vector_store
        st.session_state.rag_chain = rag_chain
        st.session_state.chunks_len = len(chunks)
        st.session_state.chat_history = []

    st.success("Document ready. Start chatting 👇")

# -------------------- CHAT DISPLAY --------------------

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

# -------------------- CHAT INPUT --------------------

if st.session_state.rag_chain:
    user_input = st.chat_input("Ask a question about the document...")

    if user_input:
        # Show user message
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.write(user_input)

        # Build conversational question
        conversation_context = ""
        for role, msg in st.session_state.chat_history[-6:]:
            if role == "user":
                conversation_context += f"User: {msg}\n"
            else:
                conversation_context += f"Assistant: {msg}\n"

        final_question = f"""
Conversation so far:
{conversation_context}

Current question:
{user_input}
"""

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                sources = retrieve_with_sources(
                    st.session_state.vector_store,
                    user_input,
                    st.session_state.chunks_len
                )

                response = st.session_state.rag_chain.invoke(final_question)
                answer = deduplicate_lines(response.content)

                st.write(answer)

        st.session_state.chat_history.append(("assistant", answer))

        # Optional: show sources
        with st.expander("Sources"):
            for i, doc in enumerate(sources, 1):
                page = doc.metadata.get("page", "N/A")
                st.markdown(f"**Source {i} (Page {page})**")
                st.write(doc.page_content[:300] + "...")
