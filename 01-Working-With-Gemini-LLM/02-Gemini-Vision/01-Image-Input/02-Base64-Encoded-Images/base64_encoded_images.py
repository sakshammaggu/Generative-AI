import base64
from google import genai
from google.genai.types import Part
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Load the image and encode it as base64
image_path = os.path.join(os.path.dirname(__file__), "local-image.jpeg")
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

client = genai.Client(api_key = GEMINI_API_KEY)
response = client.models.generate_content(
    model = "gemini-1.5-flash",
    contents = [
        "What is this image?",
        Part.from_bytes(data = base64.b64decode(base64_image), mime_type = "image/jpeg")  
    ]
)

print(response.text)