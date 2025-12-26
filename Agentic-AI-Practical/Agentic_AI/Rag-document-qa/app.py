import streamlit as st
import os

from rag_pipeline import (
    load_document,
    split_documents,
    create_vector_store,
    create_rag_chain,
    retrieve_with_sources
)

st.set_page_config(page_title="RAG Document Chat", layout="centered")

st.title("📄 RAG Document Question Answering")
st.write("Upload a document and ask questions based on its content.")

# -------------------- FILE UPLOAD --------------------

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    os.makedirs("data/uploads", exist_ok=True)
    file_path = os.path.join("data/uploads", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Document uploaded successfully.")

    # -------------------- PROCESS DOCUMENT --------------------
    with st.spinner("Processing document..."):
        docs = load_document(file_path)
        chunks = split_documents(docs)
        vector_store = create_vector_store(chunks)
        rag_chain = create_rag_chain(vector_store)

    st.success("Document processed. Ask your question below.")

    # -------------------- QUESTION INPUT --------------------
    question = st.text_input(
        "Ask a question about the document:",
        placeholder="e.g. List projects, What skills are mentioned, Summarize experience"
    )

    if question:
        with st.spinner("Generating answer..."):
            source_docs = retrieve_with_sources(vector_store, question)
            response = rag_chain.invoke(question)

        st.subheader("Answer")
        st.write(response.content)

        st.subheader("Sources")
        for i, doc in enumerate(source_docs, 1):
            page = doc.metadata.get("page", "N/A")
            st.markdown(f"**Source {i} (Page {page})**")
            st.write(doc.page_content[:300] + "...")
