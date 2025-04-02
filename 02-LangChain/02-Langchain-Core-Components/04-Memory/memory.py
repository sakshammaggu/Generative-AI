from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-flash",
    google_api_key = GOOGLE_API_KEY
)

# Define a prompt template with history placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the conversation history to answer questions."),
    MessagesPlaceholder(variable_name="history"),  # Placeholder for chat history
    ("human", "{input}")
])

# Create the base chain
chain = prompt | llm

# Initialize in-memory chat history
chat_history = InMemoryChatMessageHistory()

# Wrap the chain with message history
# We need a session ID to track the conversation (e.g., "user1")
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda: chat_history,  # Function returning the chat history
    input_messages_key = "input",  # Key for the input in the invoke dict
    history_messages_key = "history"  # Key for history in the prompt
)

# First interaction
response1 = chain_with_history.invoke(
    {"input": "My favorite color is blue."},
    config={"configurable": {"session_id": "user1"}}
)
print(response1.content)

# Second interaction
response2 = chain_with_history.invoke(
    {"input": "What’s my favorite color?"},
    config={"configurable": {"session_id": "user1"}}
)
print(response2.content)

# Check memory contents
print("\nMemory contents:")
for message in chat_history.messages:
    print(f"{message.type}: {message.content}")