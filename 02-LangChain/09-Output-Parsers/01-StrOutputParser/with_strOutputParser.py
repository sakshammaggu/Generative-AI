from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

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

parser = StrOutputParser()
chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({"topic": "Black Hole"})
print(result)