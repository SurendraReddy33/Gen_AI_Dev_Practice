from openai import OpenAI
import os
from google import genai


api_key = os.getenv("API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Explain to me AI or ML which is best"
        }
    ]
)

print(response.choices[0].message)