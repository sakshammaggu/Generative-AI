from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found in .env")
    exit(1)

@tool
def calculate_expression(expression: str) -> str:
    """Evaluates a mathematical expression using BODMAS rules and returns the result as a string."""
    try:
        expression = expression.strip()  # Remove leading/trailing whitespace
        expression = expression.replace("^", "**")  # Convert ^ to ** for exponentiation
        result = eval(expression, {"__builtins__": {}}, {"pow": pow})  # Safe eval with limited scope
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: Invalid expression ({str(e)})"

# Initialize the LLM (only for non-math responses)
llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',
    google_api_key=GOOGLE_API_KEY
)

# Define the prompt (for non-math detection)
prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a calculator assistant named CalcBot. Your job is to determine if the user's input is a valid mathematical expression.
     If the input contains numbers and operators (e.g., +, -, *, /, ^, or parentheses), respond with 'MATH_DETECTED'.
     If the input is not a math expression, respond with: 'Please provide a math expression to calculate.'
     Do not perform any calculations yourself—only classify the input."""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Create the chain
chain = prompt | llm

# Initialize chat history
chat_history = InMemoryChatMessageHistory()

# Create the chain with history
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda: chat_history,
    input_messages_key="input",
    history_messages_key="history"
)

def is_math_expression(input_str: str) -> bool:
    """Check if the input contains mathematical operators or parentheses."""
    return bool(re.search(r'[+\-*/^()]|\d', input_str))

def extract_expression(input_str: str) -> str:
    """Extract the mathematical expression from the input, if embedded in a sentence."""
    match = re.search(r'[\d+\-*/^()]+(?:\s*[\d+\-*/^()]+)*', input_str)
    return match.group(0) if match else input_str

def solve_math(user_input):
    try:
        # First, check if it looks like a math expression using regex
        if is_math_expression(user_input):
            expression = extract_expression(user_input)
            result = calculate_expression(expression)
            print("CalcBot:\n", result)
        else:
            # Use LLM to confirm non-math input
            response = chain_with_history.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": "user1"}}
            )
            content = response.content.strip()
            if content == "MATH_DETECTED":
                # Shouldn’t happen due to regex check, but handle it
                expression = extract_expression(user_input)
                result = calculate_expression(expression)
                print("CalcBot:\n", result)
            else:
                print("CalcBot:\n", content)
    except Exception as e:
        print("Error:", str(e))
        if is_math_expression(user_input):
            # Fallback in case of any error
            expression = extract_expression(user_input)
            result = calculate_expression(expression)
            print("CalcBot (Fallback):\n", result)
        else:
            print("CalcBot:\n", "Please provide a math expression to calculate.")
    print("---------------------------------------------")

def start_calculator():
    print("Welcome to CalcBot! Ask me math questions (e.g., '(8-(4+4)+(2-1))', 'What’s (2 + 3) * 4?', '5 ^ 2'), or type 'exit' to quit.")
    chat_history.clear()
    while True:
        user_input = input("Saksham: ")
        if user_input.lower() == "exit":
            print("Goodbye, Saksham!")
            break
        solve_math(user_input)

if __name__ == "__main__":
    start_calculator()