import fitz
import os
import openai
import numpy as np
import faiss
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

CHUNK_SIZE = 500
EMBED_MODEL = "text-embedding-3-small"
INDEX_FILE_PATH = "faiss.index"

def embed_chunks(text_chunks):
    embeddings = openai.embeddings.create(model=EMBED_MODEL, input = text_chunks)
    vectors = np.array([e.embedding for e in embeddings.data]).astype("float32")
    return vectors

def chunk_text(text):
    words = text.split()
    return [ " ".join(words[i: i + CHUNK_SIZE]) for i in range(0, len(words), CHUNK_SIZE)]

def extract_text_from_pdf(pdf_path):
    pages = fitz.open(pdf_path)
    full_text = "\n".join([page.get_text() for page in pages])
    return full_text

def add_document():
    pdf_path = input("Enter path of PDF file: ").strip()
    if not os.path.exists(pdf_path):
        print(f"file not found on location {pdf_path}")
        return
    text = extract_text_from_pdf(pdf_path)

    if not text:
        print("No content found. Try another pdf")
        return
    
    text_chunks = chunk_text(text)
    vectors = embed_chunks(text_chunks)

    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, INDEX_FILE_PATH)
    print("Document was indexed successfully")

def query_document():
    return True

def delete_document():
    return True

def main():
    while True:
        print("\n Select an Option: ")
        print("1. Add document to FAISS Index")
        print("2. Query Document")
        print("3. Delete Document")
        print("4. Exit")
        choice = input("please select an option (1/2/3/4): ").strip()

        if choice == 1:
            add_document()

        elif choice == 2:
            query_document()

        elif choice == 3:
            delete_document()

        elif choice == 4:
            print("Goodbye.....see you again")
            break
        else:
            print("Incorrect choice. please try again")

        

if __name__ == "__main__":
    main()
