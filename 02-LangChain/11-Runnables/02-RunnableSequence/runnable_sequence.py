from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
load_dotenv()

prompt = PromptTemplate(
    template="Write a joke about {topic}.",
    input_variables=["topic"],
)

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

chain = RunnableSequence(prompt, llm, parser)
result = chain.invoke({"topic": "programming"})
print(result)