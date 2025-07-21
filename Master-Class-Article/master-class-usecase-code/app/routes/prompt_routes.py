from fastapi import APIRouter
from app.models.prompt import PromptInput
from app.services.prompt_service import generate_and_store_service, semantic_search_service
 
router = APIRouter()
 
@router.post("/generate_store", tags=["Store Prompt + GPT2 + Embeddings"])
async def generate_and_store(data: PromptInput):
    return await generate_and_store_service(data)
 
@router.post("/search_prompt", tags=["Semantic Search"])
async def semantic_search(data: PromptInput):
    return await semantic_search_service(data)