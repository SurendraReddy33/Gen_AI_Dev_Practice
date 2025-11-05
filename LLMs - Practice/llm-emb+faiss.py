import google.generativeai as genai
import numpy as np
import faiss
import os

print(os.getenv("GEMINI_API_KEY"))

api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini with your API key
genai.configure(api_key=api_key)

# Texts to embed
texts = [
    "AI is transforming the world",
    "Machine learning is part of AI",
    "Cricket is a popular sport in India"
]

# Generate embeddings
embeddings = [
    genai.embed_content(model="models/embedding-001", content=t)["embedding"]
    for t in texts
]

# Create FAISS index
index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(np.array(embeddings))

# Query
query = "Tell me about artificial intelligence"

# Get query embedding
query_embedding = genai.embed_content(model="models/embedding-001", content=query)["embedding"]

# Search for top 2 similar results
_, results = index.search(np.array([query_embedding]), k=2)

# Print results
print("\nTop Similar Texts:")
for i in results[0]:
    print("-", texts[i])
