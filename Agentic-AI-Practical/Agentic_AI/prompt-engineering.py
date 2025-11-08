from fastapi import FastAPI , HTTPException, requests
from google import genai
from google.genai import types
from pydantic import BaseModel
import pathlib
import os
 
 
app = FastAPI(title="GenAI Prompts")
api_key = os.getenv("llm-api-key")
client = genai.Client(api_key=api_key)

class TextRequest(BaseModel):
    text: str
 
 
# Text summarization
@app.post("/summarize_text")
async def summarize_text(request: TextRequest):
   
    prompt = f"Summarize the following text:\n{request.text}"
   
    # Generate content using Google GenAI
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Part(text=prompt)]
    )
   
 
    return {"summary": response.text}
 
# Zero shot prompt  endpoint
@app.post("/zero_shot")
async def zero_shot_prompt(request : TextRequest):
    if not request.text:
        raise HTTPException(status_code=204, detail= "No text found.")
   
    #prompt = f" Translate the text into German {request.text}"
    prompt = f"Classify the sentence whether it is an postive,negative or neutral \n Text : {request.text}"
 
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=[types.Part(text = prompt)]
    )
 
    return {"Response" : response.text}
 
 
# few shot promp endpoint
@app.post("/role_based_prompt")
async def role_based_prompt(request : TextRequest):
    if not request.text:
        raise HTTPException(status_code=204, detail= "No text found.")
   
    prompt = f"""System: You are a helpful  assistant.
    User: Hi, I want to know about ice mountains
 
    Assistant: Ice mountains were formed in cold climates, completely in a frozen state. They melt during summer.
    User: Thank you
    Assistant: Do you want to know anything else?
    User: {request.text}
    Assistant :
    """
 
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=[types.Part(text = prompt)]
    )
 
    return {"Response" : response.text}
 
 
#few shot prompt
@app.post("/few_shots_prompt")
async def few_shots_prompt(request : TextRequest):
 
    if not request.text:
        raise HTTPException(status_code=204, detail="Empty response was received.")
   
    prompt = f""" Extract the cities from the text, include state they are in.
 
    user : vijayawada is having famous  bus stand , railway station.
    Model : vijayawada -Andhra Pradesh
    user : Hyderabad is the heart for IT growth.
    Model : Hyderabad: Telangana
    user   : {request.text}
    Model
    """
 
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=[types.Part(text = prompt)]
    )
 
    return {"Response" : response.text}
 
# # chain of thought prompt
@app.get("/chain_of_thought")
async def chain_of_thought_prompt():
   
    prompt = f""" A can finish a work in 18 days and B can do the same work in 15 days. B worked for 10 days and left the job. In how many days, A alone can finish the remaining work
    """
 
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=[types.Part(text = prompt)]
    )
 
    if not response.text:
        raise HTTPException(status_code=204,
                            detail="Empty prompt was given")
 
    return {"Response" : response.text}
 
 
@app.post("/pdf_qna")
async def qna_pdf(request : TextRequest): 
    # Retrieve and encode the PDF byte
    filepath = pathlib.Path('GenAI_Assignment_LangGraph_MultiAgent.pdf')
 
    prompt = request.text
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part.from_bytes(
            data=filepath.read_bytes(),
            mime_type='application/pdf',
        ),
        prompt])
    return {"Response" : response.text}


# Role-based Prompt
@app.post("/role-based")
def generate(request: TextRequest):
 
    system_prompt = "You are a friendly English teacher who explains simply."
    user_prompt = request.text
    
    # Combine system instructions + user question in a single user content block
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=system_prompt + "\n\nUser: " + user_prompt)
            ]
        )
    ]
    
    config = types.GenerateContentConfig(
        temperature=0.4
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=config
    )
    
    return {"response":response.text}

# structured output
@app.post("/structured")
def generate_response(request: TextRequest):
   
    system_prompt = "You are a friendly English teacher who explains simply."
    user_prompt = request.text
 
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Content(
                role="user",
                parts=[types.Part(text=user_prompt)]
            )
        ],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            max_output_tokens=200
        )
    )
 
    # Build structured JSON output
    structured_output = {
        "status": "success",
        "model": "gemini-2.5-flash",
        "system_instruction": system_prompt,
        "input": {
            "user_text": user_prompt
        },
        "output": {
            "answer": response.text,
            "tokens": {
                # `response.usage_metadata` is a pydantic model, not a dict. Use getattr
                # to safely access its attributes.
                "input_tokens": getattr(getattr(response, "usage_metadata", None), "input_tokens", None),
                "output_tokens": getattr(getattr(response, "usage_metadata", None), "output_tokens", None),
            }
        }
    }
 
    return structured_output
    
    

    