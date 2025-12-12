from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types
import os

api_key = os.getenv("llm-api-key")
client = genai.Client(api_key=api_key)

app = FastAPI()

class TextSummarize(BaseModel):
    text: str

@app.post("/prompt/zero-shot")
async def summarize(request: TextSummarize):
    prompt = f"""
    Divide the sentence in to tokens.
    {request.text}
"""

    response = client.models.generate_content(
        model = "gemini-2.5-pro",
        contents= prompt,
    )

    return {"Answer":response.text}