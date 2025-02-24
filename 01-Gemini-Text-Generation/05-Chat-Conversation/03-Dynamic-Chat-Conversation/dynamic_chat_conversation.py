from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key = GEMINI_API_KEY)
chat = client.chats.create(
    model = "gemini-2.0-flash"
)

print("Chat started. Type 'exit' to quit.")
while True:
    prompt = input("Enter your prompt: ")

    if prompt.lower() == "exit":
        print("Chat ended.")
        break

    try:
        response = chat.send_message(prompt)
        print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")