from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-flash",
    google_api_key = GOOGLE_API_KEY
)

prompt_template = "Write a short story about a {character} in a {setting}."
prompt = PromptTemplate.from_template(prompt_template)

chain = prompt | llm

response = chain.invoke({
    "character": "brave explorer", 
    "setting": "mysterious jungle"
})
print("Response:\n", response.content)