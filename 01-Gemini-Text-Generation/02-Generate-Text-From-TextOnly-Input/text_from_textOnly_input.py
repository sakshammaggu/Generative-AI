from google import genai
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Print waiting message
sys.stdout.write("Waiting for reply from Gemini...\r")
sys.stdout.flush()

# Make API call to Gemini
client = genai.Client(api_key = GEMINI_API_KEY)
response = client.models.generate_content(
    model = "gemini-2.0-flash",
    contents = "What is Generative AI?"
)

# Clear the waiting message
sys.stdout.write("\r" + " " * 40 + "\r")
sys.stdout.flush()

# Print the response
print("Response from Gemini:")
print("---------------------\n")
print(response.text)