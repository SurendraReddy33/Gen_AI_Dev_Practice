from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import os

# ---------- Setup ----------
api_key = os.getenv("llm-api-key")
client = genai.Client(api_key=api_key)

app = FastAPI()

# ---------- Models ----------
class SummarizeRequest(BaseModel):
    text: str
    level: str = "short"     # short / medium / detailed


# ---------- 1️⃣ Basic Summarization ----------
@app.post("/summarize/basic")
async def summarize_basic(request: SummarizeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    prompt = f"Summarize the following text clearly:\n\n{request.text}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {"summary": response.candidates[0].content.parts[0].text}


# ---------- 2️⃣ Level-Based Summarization ----------
@app.post("/summarize/level")
async def summarize_with_level(request: SummarizeRequest):
    level_prompt = {
        "short": "Summarize in 1-2 sentences.",
        "medium": "Summarize in 3-4 sentences with key ideas.",
        "detailed": "Provide a detailed summary covering all points."
    }.get(request.level.lower(), "Summarize briefly.")

    prompt = f"{level_prompt}\n\nText:\n{request.text}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {
        "level": request.level,
        "summary": response.candidates[0].content.parts[0].text
    }


# ---------- 3️⃣ Summarization + Keywords ----------
@app.post("/summarize/keywords")
async def summarize_with_keywords(request: SummarizeRequest):
    prompt = (
        f"Summarize the following text, then list 5 keywords at the end:\n\n{request.text}"
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {"summary_keywords": response.candidates[0].content.parts[0].text}


# ---------- 4️⃣ Safe Summarization (Error-Handled) ----------
@app.post("/summarize/safe")
async def safe_summarize(request: SummarizeRequest):
    try:
        prompt = f"Summarize this:\n\n{request.text}"
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return {"summary": response.candidates[0].content.parts[0].text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
