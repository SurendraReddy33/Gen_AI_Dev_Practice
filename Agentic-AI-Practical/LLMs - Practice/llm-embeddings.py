from google import genai
import os

api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)


result = client.models.embed_content(
        model="gemini-embedding-001",
        contents="What is the meaning of life?")

print(result.embeddings)