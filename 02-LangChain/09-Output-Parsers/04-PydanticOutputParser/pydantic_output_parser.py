from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

model = ChatOpenAI(model = 'gpt-4o-mini')

class Person(BaseModel):
    name: str = Field(description='Name of the person')
    age: int = Field(gt=18, description='Age of the person')
    city: str = Field(description='Name of the city the person belongs to')

pydantic_output_parser = PydanticOutputParser(pydantic_object=Person)

prompt_template = PromptTemplate(
    template='Generate the name, age and city of a fictional {place} person \n {format_instructions}',
    input_variables=['place'],
    partial_variables={'format_instructions':pydantic_output_parser.get_format_instructions()}
)

chain = prompt_template | model | pydantic_output_parser
final_result = chain.invoke({'place':'sri lankan'})
print(final_result)