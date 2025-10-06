from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os

api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

app = FastAPI()

class TextSummarize(BaseModel):
    text: str

@app.post("/text/summarize")
async def summarize(request: TextSummarize):
    prompt = f"Summarize the following text: {request.text}"

    response = client.models.generate_content(
        model = "gemini-2.5-pro",
        contents= prompt,
    )

    return {"summary": response.text}