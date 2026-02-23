# control flow runnable
# which allows you to branch your runnable execution based on the output of a previous runnable
# making conditional chains
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnablePassthrough, RunnableBranch
from dotenv import load_dotenv
load_dotenv()

prompt1 = PromptTemplate(
    template="Generate a brief report on the following topic: {topic}",
    input_variables=["topic"]
)
prompt2 = PromptTemplate(
    template="Generate a summary on report: {text}",
    input_variables=["text"]
)
llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

sequence_chain = RunnableSequence(prompt1, llm, parser)
branch_chain = RunnableBranch(
    (lambda x: len(x.split()) >= 500, RunnableSequence(prompt2, llm, parser)),
    RunnablePassthrough()
)
final_chain = RunnableSequence(sequence_chain, branch_chain)

print(final_chain.invoke({"topic": "The impact of climate change on global agriculture"}))