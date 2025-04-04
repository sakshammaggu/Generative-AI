from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables from a .env file (containing the API key)
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

"""
Initialize the Gemini Flash model
Logic:
- ChatGoogleGenerativeAI is a wrapper that connects to Google's Gemini API
- model="gemini-1.5-flash" specifies the specific version of Gemini to use
- google_api_key passes the authentication key to access the API
Communication:
- This object (llm) will send prompts to Gemini Flash and receive responses via API calls
"""
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY
)

"""
Define the prompt template for the code debugger
Logic:
- ChatPromptTemplate.from_messages creates a structured prompt with multiple parts
- List contains:
  1. System message: Sets the assistant's role and behavior
     - The prompt strictly instructs the assistant to only help with debugging/coding questions.
     - If a user asks anything unrelated (e.g., travel, food, movies), the assistant will politely refuse.
  2. MessagesPlaceholder: Reserves a spot for conversation history
  3. Human message: Placeholder for current user input
Communication:
- The template is a blueprint that gets filled with history and user input later
- It tells Gemini Flash how to interpret the input in the right context
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are 'Code Bug Detective', a helpful but strict assistant who ONLY helps with programming, debugging, and code error questions. "
     "If a user asks anything that is NOT related to code or debugging, politely refuse and remind them that you are only trained for debugging support."
     "Remember the users name and use it throughout the conversation."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

"""
Create the base chain (a runnable sequence)
Logic:
- The | operator (pipe) combines the prompt template and LLM into a sequence
- Steps: Format the prompt -> Send to Gemini Flash -> Get response
Communication:
- prompt_template prepares the input, then passes it to llm for processing
- This is the core workflow without memory yet
"""
chain = prompt | llm

"""
Define a function to interact with the assistant
Logic:
- Takes user input and chat_history as parameters
- Wraps the chain with RunnableWithMessageHistory to maintain ongoing session memory
- Invokes the chain with the input and session config
- Prints the response from Gemini Flash
Communication:
- User input is formatted into the prompt with history
- Sent to Gemini Flash via the chain, response is extracted and displayed
"""
def debug_code_assistant(user_input, chat_history):
    chain_with_history = RunnableWithMessageHistory(
        chain,                                 # The base LLM pipeline
        lambda: chat_history,                  # Supplies the memory store (chat history)
        input_messages_key="input",            # Where to inject the user input
        history_messages_key="history"         # Where to store/retrieve chat history
    )
    response = chain_with_history.invoke(
        {"input": user_input},                 # Pass the user input dynamically
        config={"configurable": {"session_id": "coder1"}}  # Identifies the session uniquely
    )
    print("Response:\n", response.content)     # Output the assistant's response
    print("---------------------------------------------")

"""
Define a function to start an interactive conversation
Logic:
- Prints a welcome message
- Creates a new chat history instance for this run (isolated per user session)
- Enters a loop to continuously get user input from the terminal
- Exits if the user types "exit"
- Passes input and history to debug_code_assistant
Communication:
- Acts as the user interface, ensuring a fresh history each run
"""
def start_debugging():
    print("Welcome to the Code Bug Detective! Describe your bug, or type 'exit' to quit.")
    chat_history = InMemoryChatMessageHistory()  # New chat history instance per session
    while True:
        user_input = input("Saksham: ")         # Prompt the user for input
        if user_input.lower() == "exit":        # Exit condition
            print("Goodbye!")
            break
        debug_code_assistant(user_input, chat_history)  # Send input to assistant

if __name__ == "__main__":
    start_debugging()