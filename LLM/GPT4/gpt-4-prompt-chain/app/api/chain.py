from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI # pip install openai
import os

router = APIRouter()
client = OpenAI (api_key = os.getenv("OPENAI_API_KEY")) # always read from Enviroments

class TextInput (BaseModel):
    text: str
    language: str = "hi"



# Original  : He go to market yesterday for buying vegetables but forget to took money.
# Summary : He went to the market yesterday to buy vegetables but forgot to bring money.


@router.post ("/prompt_chain")
async def prompt_chain (input: TextInput):

    # Step 1 : Summerize Role -> User Input 
    summary = client.chat.completions.create (
        model = "gpt-4", 
        messages = [
            {"role": "system", "content" : "Summarize the following text"},
            {"role" : "user","content" : input.text}
        ], 
        temperature = 0.4
    ).choices[0].message.content.strip()


    # Step 2 : Grammar Fix
    
    improved_text = client.chat.completions.create (
    model = "gpt-4", 
    messages = [
        {"role": "system", "content" : "Improve grammar and clarity of this text"},
        {"role" : "user","content" : input.text}
    ], 
    temperature = 0.3
).choices[0].message.content.strip()

    # Step 3 : Translate
    translated_text = client.chat.completions.create (
    model = "gpt-4", 
    messages = [
        {"role": "system", "content" : f"Translate the following text to {input.language}."},
        {"role" : "user","content" : improved_text}
    ], 
    temperature = 0.3
    ).choices[0].message.content.strip()

    return {
        "summary" : summary,
        "improved_text" : improved_text,
        "translated_text" : translated_text
    }

    