from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-flash",
    google_api_key = GOOGLE_API_KEY,
    temperature = 0.3,
    max_tokens = 100
)

try:
    creative_response = llm.invoke("Write a haiku about the ocean.")
    print("\nHaiku:")
    print(creative_response.content)
except Exception as e:
    print(f"Error: {e}")