from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from langchain.schema.runnable import RunnableBranch, RunnableLambda
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

class Feedback(BaseModel):
    sentiment: Literal["Positive", "Negative"] = Field(
        description="Give the sentiment of the feedback"
    )

parser_with_pydantic = PydanticOutputParser(pydantic_object=Feedback)

prompt1 = PromptTemplate(
    template="Classify the sentiment of following feedback text as Positive or Negative: \n {feedback} \n {format_instruction}",
    input_variables=["feedback"],
    partial_variables={"format_instruction": parser_with_pydantic.get_format_instructions()}
)

classifier_chain = prompt1 | model | parser_with_pydantic

classifier_chain_result = classifier_chain.invoke({'feedback': "The product was great and met all my expectations!"}).sentiment
print(f"Classifier Chain Result: {classifier_chain_result}")

prompt_positive = PromptTemplate(
    template="Write the appropriate response to the positive feedback: \n {positive_feedback}",
    input_variables=["positive_feedback"]
)
prompt_negative = PromptTemplate(
    template="Write the appropriate response to the negative feedback: \n {negative_feedback}",
    input_variables=["negative_feedback"]
)

branch_chain = RunnableBranch(
    ( lambda x: x.sentiment == "Positive", prompt_positive | model | parser ),
    ( lambda x: x.sentiment == "Negative", prompt_negative | model | parser ),
    RunnableLambda(lambda x: "Could not find sentiment.")
)

chain = classifier_chain | branch_chain
result = chain.invoke({'feedback': "The product was great and met all my expectations!"})
print(f"Final Response: {result}")