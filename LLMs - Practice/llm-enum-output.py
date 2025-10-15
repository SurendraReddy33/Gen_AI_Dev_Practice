from google import genai
import enum
import os

api_key = os.getenv("API_KEY")

class Genre(enum.Enum):
    ACTION = "Action"
    DRAMA = "Drama"
    COMEDY = "Comedy"
    HORROR = "Horror"
    SCI_FI = "Sci-Fi"

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="The movie is about a team of astronauts traveling to another galaxy to save humanity.",
    config={
        'response_mime_type': 'text/x.enum',
        'response_schema': Genre,
    },
)

print(response.text)
# SCI_FI