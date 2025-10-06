from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

load_dotenv()

model = ChatOpenAI(model = 'gpt-4o-mini')

schema = [
    ResponseSchema(name="fact_1", description="Fact 1 about the topic"),
    ResponseSchema(name="fact_2", description="Fact 2 about the topic"),
    ResponseSchema(name="fact_3", description="Fact 3 about the topic"),
]

structured_output_parser = StructuredOutputParser.from_response_schemas(schema)

prompt_template = PromptTemplate(
    template = 'Give 3 facts about {topic} \n {format_instructions}',
    input_variables = ['topic'],
    partial_variables = {"format_instructions": structured_output_parser.get_format_instructions()},
)

chain = prompt_template | model | structured_output_parser
result = chain.invoke({"topic": "Black Holes"})
print(result)