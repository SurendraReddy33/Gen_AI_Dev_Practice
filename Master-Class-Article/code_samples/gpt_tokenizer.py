from transformers import GPT2Tokenizer
 
# Load the GPT-2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
 
# Input text
text = "Hello, my name is Surendra!"
 
# Tokenize the text
tokens = tokenizer.tokenize(text)
print("Tokens:", tokens)
 
# Convert tokens to IDs
token_ids = tokenizer.convert_tokens_to_ids(tokens)
print("Token IDs:", token_ids)
 
# Encode full sentence with padding and truncation
encoded = tokenizer.encode_plus(
    text,
    return_tensors="pt",
    padding='max_length',
    max_length=10,
    truncation=True
)
print("Encoded input IDs:", encoded['input_ids'])