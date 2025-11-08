# basic response
from google import genai
import os

api_key = os.getenv("llm-api-key")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
    )

print(response.text)



# Extra functionalties response
from google import genai
from google.genai import types
import os
 
api_key = os.getenv("llm-api-key")
client = genai.Client(api_key=api_key)
 
prompt = input("Enter your prompt : ").strip()
 
config = types.GenerateContentConfig(
    temperature= 0.2,
    candidate_count=1,
    thinking_config=types.ThinkingConfig(
        thinking_budget=300
    )
)
 
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,  # string or list of TypeContent
    config=config,
)
print(response.text)


# System Instruction with user input
from google import genai
from google.genai import types
import os
 
api_key = os.getenv("llm-api-key")
client = genai.Client(api_key=api_key)

 
system_instruction= input("Enter system instruction : ").strip()
content = input("Enter content : ").strip()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    # `contents` must be passed as an argument to generate_content (not inside config).
    contents=content,
    config=types.GenerateContentConfig(
        # correct spelling: `temperature`
        temperature=0.2,
        max_output_tokens=256,
        system_instruction=system_instruction,
    ),
)
 
print(response.text)