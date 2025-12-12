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

@app.post("/prompt/few-shots")
async def summarize(request: TextSummarize):
    prompt = f"""
    Sort the animals from biggest to smallest.
    Question: Sort Tiger, Bear, Dog
    Answer: Bear > Tiger > Dog
    Question: Sort Cat, Elephant, Zebra
    Answer: Elephant > Zebra > Cat
    Question: {request.text}
    Answer:
"""

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents= prompt,
    )

    return {"Answer":response.text}