from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

model = ChatOpenAI(model = 'gpt-4o-mini')
jsonOutputParser = JsonOutputParser()

promptTemplate = PromptTemplate(
    template = 'Give me the name, age and city of a fictional person \n {format_instructions}',
    input_variables = [],
    partial_variables = {"format_instructions": jsonOutputParser.get_format_instructions()},
)

prompt = promptTemplate.format()
response = model.invoke(prompt)
result = jsonOutputParser.parse(response.content)
print(result)
print(type(result))

chain = promptTemplate | model | jsonOutputParser
newResult = chain.invoke({})
print(newResult)