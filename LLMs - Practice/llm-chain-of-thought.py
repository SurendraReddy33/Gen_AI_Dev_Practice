from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types                                 
import os
from IPython.display import Markdown                            

api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)                                                 

app = FastAPI()

class TextSummarize(BaseModel):
    text: str

@app.get("/prompt/chain-of-thought")
async def summarize():
    prompt = """
  Question: 11 factories can make 22 cars per hour. How much time would it take 22 factories to make 88 cars?
  Answer: A factory can make 22/11=2 cars per hour. 22 factories can make 22*2=44 cars per hour. Making 88 cars would take 88/44=2 hours. The answer is 2 hours.
  Question: 5 people can create 5 donuts every 5 minutes. How much time would it take 25 people to make 100 donuts?
  Answer:
"""

    response = client.models.generate_content(
        model = "gemini-2.5-pro",
        contents= prompt,
    )

    return {response.text}