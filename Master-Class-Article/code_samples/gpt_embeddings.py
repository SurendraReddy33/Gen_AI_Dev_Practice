## 🧪 Sample Code: Generate Sentence Embedding using GPT-2
 
from transformers import GPT2Tokenizer, GPT2Model
import torch
 
# Load GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")
 
# Important: Set model to evaluation mode
model.eval()
 
# Input sentence
text = "Vectors are powerful in NLP."
 
# Tokenize input
inputs = tokenizer(text, return_tensors="pt")
 
# Generate embeddings (last hidden state)
with torch.no_grad():
    outputs = model(**inputs)
 
# Take mean of token embeddings to get sentence-level vector
embedding = outputs.last_hidden_state.mean(dim=1)
 
print("Sentence Embedding:", embedding)