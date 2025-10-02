from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatOpenAI(model = 'gpt-4o-mini')

# 1st Prompt -> detailed report
template1 = PromptTemplate(
    template="Write a 100 word report on {topic}",
    input_variables=["topic"],
)

# 2nd Prompt -> summarize the report in a single sentence
template2 = PromptTemplate(
    template="Write a 5 line summary on following text: /n {text}",
    input_variables=["text"],
)

prompt1 = template1.invoke({"topic": "Black Hole"})
result1 = model.invoke(prompt1)

prompt2 = template2.invoke({"text": result1.content})
result2 = model.invoke(prompt2)
print(result2.content)