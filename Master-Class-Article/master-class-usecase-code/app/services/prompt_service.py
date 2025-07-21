from app.models.prompt import PromptInput
from app.loaders.model_loader import gpt2_tokenizer, gpt2_model, embedder, collection
from app.utils.logger import get_logger
from app.utils.decorators import handle_exceptions
import torch
 
logger = get_logger(__name__)
 
@handle_exceptions
async def generate_and_store_service(data: PromptInput):
    prompt_text = data.prompt
    logger.info(f"Received prompt: {prompt_text}")
 
    # Tokenization
    tokens = gpt2_tokenizer.encode(prompt_text, return_tensors="pt")[0].tolist()
    tokenized_words = gpt2_tokenizer.tokenize(prompt_text)
 
    # Generate GPT2 response
    gpt_input = torch.tensor([tokens])
    gpt_output = gpt2_model.generate(gpt_input, max_length=100)
    generated_text = gpt2_tokenizer.decode(gpt_output[0], skip_special_tokens=True)
    logger.info(f"Generated text: {generated_text}")
 
    # Get embeddings
    embedding = embedder.encode(prompt_text).tolist()
 
    # Store in MongoDB
    doc = {
        "prompt": prompt_text,
        "tokens": [tokens, tokenized_words],
        "embedding": embedding,
        "gpt2_response": generated_text,
    }
    collection.insert_one(doc)
    logger.info("Document inserted into MongoDB")
 
    return {
        "message": "Stored successfully",
        "prompt": prompt_text,
        "gpt2_response": generated_text,
    }
 
 
@handle_exceptions
async def semantic_search_service(data: PromptInput):
    query_prompt = data.prompt
    logger.info(f"Semantic search for: {query_prompt}")
 
    query_embed = embedder.encode(query_prompt, convert_to_tensor=True)
 
    docs = list(collection.find({}, {"_id": 0, "prompt": 1, "gpt2_response": 1, "embedding": 1}))
    if not docs:
        logger.warning("No documents found in database")
        return {"message": "No data in database"}
 
    stored_embeddings = torch.tensor([doc["embedding"] for doc in docs])
    similarities = torch.nn.functional.cosine_similarity(query_embed, stored_embeddings)
    top_index = torch.argmax(similarities).item()
    match = docs[top_index]
 
    logger.info(f"Top match: {match['prompt']} (Score: {similarities[top_index].item():.4f})")
 
    return {
        "closest_prompt": match["prompt"],
        "response": match["gpt2_response"],
        "similarity_score": round(similarities[top_index].item(), 4),
    }