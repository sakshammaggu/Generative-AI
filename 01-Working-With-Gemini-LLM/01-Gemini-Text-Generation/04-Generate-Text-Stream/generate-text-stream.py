from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key = GEMINI_API_KEY)
response = client.models.generate_content_stream(
    model = "gemini-2.0-flash",
    contents = ["Explain how AI works"]
)

print("Response from Gemini:")
print("---------------------\n")
for chunk in response:
    print(chunk.text, end="")