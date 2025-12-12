# Problem Statement - 
# You have a Huge Text file -> input.txt 
# Chunk data = 100 tokens
# 1000 Tokens  => Create a Batch -> 100 Tokens 
# 1 Call with 1000 Tokens  : 10 Calls with 100 tokens 
# 10 Calls with 100 tokens  : 20 Calls with 50 tokens 
# Get mean Embedding (Average)


# 1. Read the Input file
# 2. Get the  Tokens (Assume we have 1000 tokens)
# 2. Set Chunk Size = 100
# 3. Get First 100 Tokens (Remaining  900)
# 4. Get the  Ids
# 5. Send to Model 
# 6. Get the Embedding  for first 100
# 7. Process them or Save or print or bla bla bla 
# 8. Goto Step 3

from transformers import GPT2Tokenizer, GPT2Model
import torch
import csv

with open ("input.txt", "r", encoding="utf-8") as f:
    file_text = f.read().strip() # read all the file content and remove L and T spaces

print  (f" File content are : {file_text}")

tokenizer = GPT2Tokenizer.from_pretrained("gpt2") # Get the tokenizer 
base_model = GPT2Model.from_pretrained("gpt2")

# Pass the content of file to the GPT2Tokenizer
token_list = tokenizer.encode(file_text) #  Gets the token [token ids format]

print  (f"found {len(token_list)} tokens")
print (f"Encoded Tokens are : {token_list}")

chunk_size = 50

for i in range(0, len(token_list),chunk_size ): # start =0, end=171, 100
    chunked_token = token_list[i:i + chunk_size]

    model_input = torch.tensor([chunked_token])

    #print (f" Chunk Obtained {model_input}")

    with torch.no_grad():
         model_output =  base_model(model_input)
         embeddings = model_output.last_hidden_state # shape: [i, chunk_size, 768]
         #print (f"last_hidden : {embeddings} ")

         mean_embeddings = embeddings.mean(dim = 1) # # shape: [i, 768]

         #print (f" Average Embeddings : {mean_embeddings}")

    chunked_text = tokenizer.decode(chunked_token) 
    print (f" Decoded Chunks {chunked_text}")
