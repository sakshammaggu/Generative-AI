from google import genai
from google.genai.types import Part
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

audio_path = os.path.join(os.path.dirname(__file__), "sample_audio.mp3")
with open(audio_path, "rb") as audio_file:
    audio_content = audio_file.read()

client = genai.Client(api_key = GEMINI_API_KEY)
response = client.models.generate_content(
    model = "gemini-1.5-flash",
    contents = [
        "Describe the audio content in brief.",
        Part.from_bytes(
            data = audio_content,
            mime_type = "audio/mp3"
        )
    ]
)

print(response.text)