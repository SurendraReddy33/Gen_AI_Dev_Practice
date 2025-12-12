from transformers import GPT2Tokenizer
import os
from google import genai

api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

# Load a tokenizer (GPT-2 in this case)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Original text
text = "Hello Surendra, how are you?"

# Step 1: Tokenization (text → tokens)
tokens = tokenizer.tokenize(text)
token_ids = tokenizer.encode(text)

print("Tokens:", tokens)
print("Token IDs:", token_ids)

# Step 2: Detokenization (tokens → text)
detokenized_text = tokenizer.decode(token_ids)

print("Detokenized Text:", detokenized_text)
