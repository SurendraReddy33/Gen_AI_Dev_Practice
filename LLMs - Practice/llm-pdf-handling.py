from google import genai
from google.genai import types
import httpx
import os

api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

doc_url = "https://arxiv.org/pdf/1706.03762"

# Retrieve and encode the PDF byte
doc_data = httpx.get(doc_url).content

prompt = "How much count of s letter had in this document?"
response = client.models.generate_content(
  model="gemini-2.5-pro",
  contents=[
      types.Part.from_bytes(
        data=doc_data,
        mime_type='application/pdf',
      ),
      prompt])
print(response.text)