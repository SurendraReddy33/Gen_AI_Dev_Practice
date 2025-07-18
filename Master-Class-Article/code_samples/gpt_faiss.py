import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
 
# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModel.from_pretrained("gpt2")
model.eval()
 
# Generate vector (example for single sentence)
sentence = "Hello world!"
inputs = tokenizer(sentence, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1).numpy()
 
# Create FAISS index
index = faiss.IndexFlatL2(embedding.shape[1])
index.add(embedding)
 
# Search
D, I = index.search(embedding, k=1)
print("Distances:", D)
print("Indices:", I)

 