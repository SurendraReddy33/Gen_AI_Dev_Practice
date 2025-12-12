from google import genai
from google.genai import types
import httpx
import os
from fastapi import FastAPI
from pydantic import BaseModel

api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

app = FastAPI()

class TextSummarize(BaseModel):
    text: str

doc_url = "https://arxiv.org/pdf/1706.03762"

@app.get("/text/pdf")
async def summarize():
    # Retrieve and encode the PDF byte
    doc_data = httpx.get(doc_url).content

    prompt = "Prepare me a neat and clear notes from this document by removing unnecessary and targeting important things"
    response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
      types.Part.from_bytes(
        data=doc_data,
        mime_type='application/pdf',
      ),
      prompt])
    return(response.text)




