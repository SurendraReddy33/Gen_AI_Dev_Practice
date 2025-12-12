from transformers import GPT2Tokenizer, GPT2Model
import torch
import torch.nn.functional as F

query = "I enjoy learning Python"

# List of possible candidate sentences
candidates = [
"Python is a powerful language", 
"Bananas are rich is potassium",
"Studying Python is enjoyable",
"The weather is nice today",
"I love Programing in Java"
] 

# Get the mean embedding (From Full Embeddings) -> Tokens  -> Model 

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")

def get_mean_embeddings (input_text):
    """
    Gets the mean embedding from the input_text

    Args:
        input_text : Text to get the mean embedding
    """
    tokens = tokenizer(input_text, return_tensors="pt") # Gets the result in PY Tensor format
    with torch.no_grad(): # Load the model for basic operations and not for training
        model_output = model(**tokens) # In the PY- TF format
        full_embeddings = model_output.last_hidden_state
        mean_embeddings = full_embeddings.mean(dim=1)
        return mean_embeddings

query_embedding = get_mean_embeddings(query)

results = []
for candidate in candidates:
    mean_embedding = get_mean_embeddings(candidate)
    score = F.cosine_similarity(query_embedding,mean_embedding).item()
    results.append((candidate, score))

results.sort(key=lambda x: x[1], reverse=True)

print (f"\nQuery is : {query} \n")
for candidate, score in results:
    print(f"{score:.4f} → {candidate}")


