from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key = GEMINI_API_KEY)
response = client.models.generate_content(
    model = "gemini-2.0-flash",
    contents = ["Explain how AI works"],
    config = types.GenerateContentConfig(
        temperature = 0.5, # Controls randomness in the output.
        max_output_tokens = 500, # Maximum number of tokens to generate.
        top_p = 0.9, # Controls diversity in the output.
    )
)

print(response.text)