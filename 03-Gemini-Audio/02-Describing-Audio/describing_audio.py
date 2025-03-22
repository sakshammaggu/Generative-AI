"""
This script demonstrates how to use Google's Gemini AI model to analyze and describe audio content.
It takes an MP3 audio file as input and uses Gemini's multimodal capabilities to generate a description
of the audio content. The script:
1. Loads an audio file from the local directory
2. Sends the audio content to Gemini AI
3. Gets back a text description of what the audio contains
This can be useful for audio content analysis, transcription verification, or automated audio description generation.
"""

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