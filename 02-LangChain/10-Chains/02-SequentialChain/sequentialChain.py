from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

prompt1 = PromptTemplate(
    template='Write a short report about: {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Give 5 pointer summary about the report: {report}',
    input_variables=['report']
)

parser = StrOutputParser()

chain = prompt1 | llm | parser | prompt2 | llm | parser

result = chain.invoke({'topic': 'AI'})
print(result)