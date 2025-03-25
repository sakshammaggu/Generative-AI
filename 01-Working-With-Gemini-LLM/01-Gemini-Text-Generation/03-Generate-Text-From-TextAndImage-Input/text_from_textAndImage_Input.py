from google import genai
from PIL import Image
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Print waiting message
sys.stdout.write("Waiting for reply from Gemini...\r")
sys.stdout.flush()

client = genai.Client(api_key = GEMINI_API_KEY)

image_path = os.path.join(os.path.dirname(__file__), "gemini_image.jpeg")
print("Image Path:", image_path)  
image = Image.open(image_path)

response = client.models.generate_content(
    model = "gemini-2.0-flash",
    contents = [image, "Tell Me about this image?"]
)

# Print the response
print("Response from Gemini:")
print("---------------------\n")
print(response.text)