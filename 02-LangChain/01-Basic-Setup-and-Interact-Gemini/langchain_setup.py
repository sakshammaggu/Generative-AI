from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-flash",
    google_api_key = GEMINI_API_KEY,
    temperature=0.7
)

response = llm.invoke("Hello! What can you do for me today?")
print(response.content)