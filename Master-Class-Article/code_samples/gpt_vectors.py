from transformers import GPT2Tokenizer, GPT2Model
import torch
 
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")
 
text = "Vectors are powerful in NLP."
tokens = tokenizer(text, return_tensors='pt')
with torch.no_grad():
    output = model(**tokens)
 
# Get the sentence vector by averaging token embeddings
sentence_vector = output.last_hidden_state.mean(dim=1)
print(sentence_vector)