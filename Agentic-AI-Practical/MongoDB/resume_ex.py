import os
import fitz  # PyMuPDF
import faiss
import numpy as np
from transformers import GPT2Tokenizer, GPT2Model, GPT2LMHeadModel
import torch
from sklearn.preprocessing import normalize
 
# Load GPT-2 tokenizer and models
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
embedding_model = GPT2Model.from_pretrained("gpt2")
lm_model = GPT2LMHeadModel.from_pretrained("gpt2")
 
embedding_model.eval()
lm_model.eval()
 
tokenizer.pad_token = tokenizer.eos_token
embedding_model.pad_token_id = tokenizer.eos_token_id
lm_model.pad_token_id = tokenizer.eos_token_id
 
PDF_FOLDER = "resumes"
dimension = 768  # GPT-2 hidden size
faiss_index = faiss.IndexFlatL2(dimension)
chunk_metadata = []
 
#  Load and clean text from PDF
def load_pdf_text(pdf_path):
    pdf_doc = fitz.open(pdf_path)
    return "\n".join([" ".join(page.get_text().split()) for page in pdf_doc])  # clean spaces/newlines
 
# #  Chunk text
# def chunk_text(text, chunk_size=200):
#     words = text.split()
#     return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
 
# Get embedding from GPT-2 using last token (like EOS)
def embed_with_gpt2(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = embedding_model(**inputs)
    last_hidden = outputs.last_hidden_state.squeeze(0)  # [seq_len, hidden_size]
    embedding = last_hidden[-1]  # Use final token's vector
    return embedding.numpy()
 
#  Index all resume chunks
def index_resumes():
    global chunk_metadata
    chunk_metadata.clear()
    vectors = []
 
    for filename in os.listdir(PDF_FOLDER):
        if filename.endswith(".pdf"):
            text = load_pdf_text(os.path.join(PDF_FOLDER, filename))
            # chunks = chunk_text(text)
            for chunk in text:
                embedding = embed_with_gpt2(chunk)
                vectors.append(embedding)
                chunk_metadata.append({
                    "filename": filename,
                    "chunk": chunk
                })
 
    if vectors:
        vectors_np = normalize(np.vstack(vectors).astype('float32'))
        faiss_index.add(vectors_np)
        print(f" Indexed {len(chunk_metadata)} chunks from resumes.")
    else:
        print(" No PDFs found or no chunks generated.")
 
# 🔍 Query resumes + generate answer using GPT-2
def query_resumes(query, top_k=3):
    if faiss_index.ntotal == 0:
        print(" Index is empty. Run option 1 first.")
        return
 
    query_embedding = embed_with_gpt2(query)
    query_embedding = normalize(np.expand_dims(query_embedding, axis=0).astype('float32'), axis=1)
 
    distances, indices = faiss_index.search(query_embedding, top_k)
 
    print(f"\n Top {top_k} matches for: \"{query}\"\n")
 
    for i, idx in enumerate(indices[0]):
        if idx == -1: continue
        match = chunk_metadata[idx]
        chunk = match['chunk']
 
        # Create prompt
        prompt = f"Answer this question: {query}\n\nBased on the following resume content:\n{chunk}\n\nAnswer:"
        inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
 
        with torch.no_grad():
            output = lm_model.generate(
                inputs,
                max_length=500,
                do_sample=True,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                num_return_sequences=1
            )
            answer = tokenizer.decode(output[0], skip_special_tokens=True).replace(prompt, '').strip()
 
        print(f"{i + 1}. File: {match['filename']}")
        print(f" Distance: {distances[0][i]:.4f}")
        print(f" Answer: {answer}")
        print("-" * 50)
 
# Main menu
def main():
    print("\n=== GPT-2 + FAISS Resume Search & Q&A ===")
    while True:
        print("\n1. Index resumes")
        print("2. Ask a question")
        print("3. Exit")
        choice = input("Choose an option: ")
 
        if choice == "1":
            index_resumes()
        elif choice == "2":
            query = input("Enter your question: ")
            query_resumes(query)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
 
if __name__ == "__main__":
    main()
 