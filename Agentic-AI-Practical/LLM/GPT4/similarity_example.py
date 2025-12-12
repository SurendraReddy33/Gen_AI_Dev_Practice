# Steps : 
# 1. Read the Sentence 1 - Get Token -> Get Embeddings -> Get Mean Embedding
# 2. Read the Sentence 2 - Get Token -> Get Embeddings -> Get Mean Embedding  

from transformers import GPT2Tokenizer, GPT2Model
import torch
import torch.nn.functional as F

# Define model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")

def get_mean_embedding (input_text):
    tokens = tokenizer(input_text, return_tensors="pt")

    with torch.no_grad():
        outputs = model (**tokens)
    
    full_embeddings = outputs.last_hidden_state # [1, tokens, 768]
    mean_embeddings = full_embeddings.mean(dim=1) # [1, 768]
    return mean_embeddings   

# Sentences to compare for similirity
# Load from File - Two files File A, File B
sentence1 = "I enjoy learning Python" # [1,4, 768]
sentence2 = "I enjoy learning Cooking" # [1,4, 768]

first_sentence_embedding = get_mean_embedding(sentence1)
second_sentence_embedding = get_mean_embedding(sentence2)

# print (f"Sentence1 mean embedding : {sentence1} {first_sentence_embedding}")
# print (f"Sentence2 mean embedding : {sentence1} {second_sentence_embedding}")

# Compare the COSINE SIMILARITY beteen towo vectors
# It measures how similar two vectors are based on Angle and Not the Size
similarity = F.cosine_similarity (first_sentence_embedding,second_sentence_embedding).item()

print  (f"Sentence1 : {sentence1} ")
print  (f"Sentence2 : {sentence2} ")
print  (f"Cosine Similarity : {similarity:.4f} (1 = Very Similar, 0 = different ) ")

