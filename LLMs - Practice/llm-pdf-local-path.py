from google import genai
from google.genai import types
import pathlib
import os


api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

# Retrieve and encode the PDF byte
filepath = pathlib.Path('C:/Users/svcs/Downloads/Surendra_Reddy_Gandra_Python_Developer.pdf')

prompt = "What are the projects mentioned in this document?"
response = client.models.generate_content(
  model="gemini-2.5-pro",
  contents=[
      types.Part.from_bytes(
        data=filepath.read_bytes(),
        mime_type='application/pdf',
      ),
      prompt])
print(response.text)