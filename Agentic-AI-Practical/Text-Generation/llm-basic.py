from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os

api_key = os.getenv("llm-api-key")
client = genai.Client(api_key=api_key)

app = FastAPI()


class TextRequest(BaseModel):
    prompt: str


# 1️⃣ Basic Text Generation
@app.get("/text/basic")
async def basic_text():
    prompt = "Write a 2-line motivational quote about learning AI."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {"result": response.text}


# 2️⃣ Dynamic User Input Generation
@app.post("/text/generate")
async def generate_text(request: TextRequest):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Generate a short paragraph about {request.prompt}"
    )
    return {"result": response.text}


# 3️⃣ Prompt Template Example
@app.post("/text/template")
async def prompt_template(request: TextRequest):
    prompt = f"Explain the importance of {request.prompt} in 3 sentences."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {"result": response.text}


# 4️⃣ Controlled Creativity Example
@app.post("/text/creative")
async def creative_text(request: TextRequest):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Write a creative story about {request.prompt}.",
        config={
            "temperature": 0.8, 
            "max_output_tokens": 100
        }
    )
    return {"result": response.text}


# 5️⃣ Error Handling Example
@app.post("/text/safe")
async def safe_generate(request: TextRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Summarize this: {request.prompt}"
        )
        return {"result": response.text}
    except Exception as e:
        return {"error": str(e)}
