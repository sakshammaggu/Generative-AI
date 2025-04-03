from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
import os

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
Define the prompt template for the travel assistant
Logic:
- ChatPromptTemplate.from_messages creates a structured prompt with multiple parts
- List contains:
  1. System message: Sets the assistant's role and behavior
  2. MessagesPlaceholder: Reserves a spot for conversation history
  3. Human message: Placeholder for user input
Communication:
- The template is a blueprint that gets filled with history and user input later
- It tells Gemini Flash how to interpret the input in context
"""
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly travel assistant. Use the conversation history to personalize suggestions and remember the user's name."),
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
chain = prompt_template | llm

"""
Initialize the in-memory chat history
Logic:
- InMemoryChatMessageHistory creates an object to store the conversation
- It holds a list of messages (human and AI) in memory during the session
Communication:
- This will be linked to the chain to provide context across interactions
"""
chat_history = InMemoryChatMessageHistory()

"""
Wrap the chain with conversation history
Logic:
- RunnableWithMessageHistory adds memory to the base chain
- Parameters:
  - chain: The base prompt | llm sequence
  - lambda: chat_history: A function returning the history object
  - input_messages_key: Maps user input to the "input" placeholder
  - history_messages_key: Maps chat history to the "history" placeholder
Communication:
- Before invoking the chain, it injects the chat history into the prompt
- Ensures Gemini Flash sees prior messages for context
"""
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda: chat_history,
    input_messages_key="input",
    history_messages_key="history" 
)

"""
Define a function to interact with the assistant
Logic:
- Takes user input as a parameter
- Invokes the chain with the input and session config
- Prints the response from Gemini Flash
Communication:
- User input is formatted into the prompt with history
- Sent to Gemini Flash via the chain, response is extracted and displayed
"""
def talk_to_assistant(user_input):
    response = chain_with_history.invoke(
        {"input": user_input},  # Dictionary with input for the prompt
        config={"configurable": {"session_id": "traveler1"}}  # Session ID for history tracking
    )
    print("Response:\n", response.content)  # Extract text from AIMessage object

"""
Define a function to start an interactive conversation
Logic:
- Prints a welcome message
- Enters a loop to continuously get user input from the terminal
- Exits if the user types "exit"
- Otherwise, passes input to talk_to_assistant
Communication:
- Acts as the user interface, bridging terminal input to the LangChain system
- Keeps the conversation flowing dynamically
"""
def start_conversation():
    print("Welcome to the Travel Assistant! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")  # Capture user input from terminal
        if user_input.lower() == "exit":  # Check for exit condition
            print("Goodbye!")
            break
        talk_to_assistant(user_input)  # Send input to the assistant

if __name__ == "__main__":
    start_conversation()