from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key = GEMINI_API_KEY)
chat = client.chats.create(
    model = "gemini-2.0-flash"
)

response = chat.send_message_stream("Explain AI in simple terms in 100 words.")
for chunks in response:
    print(chunks.text, end = "")
print("--------------------")

response = chat.send_message_stream("Explain Generative AI in simple terms in 100 words")
for chunks in response:
    print(chunks.text, end = "")
print("--------------------")

for message in chat._curated_history:
    print(f'role - ', message.role, end=": ")
    print(message.parts[0].text)