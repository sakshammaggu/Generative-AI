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

prompt_template = "Tell me a {adjective} fact about {subject}"
prompt = PromptTemplate.from_template(prompt_template)

prompt_fill_1 = prompt.format(adjective="surprising", subject="elephants")
prompt_fill_2 = prompt.format(adjective="funny", subject="penguins")

response_1 = llm.invoke(prompt_fill_1)
print("Response 1: \n", response_1.content)
response_2 = llm.invoke(prompt_fill_2)
print("Response 2: \n", response_2.content)