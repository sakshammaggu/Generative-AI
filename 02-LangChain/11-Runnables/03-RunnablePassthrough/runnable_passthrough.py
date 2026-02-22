from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnablePassthrough, RunnableParallel
from dotenv import load_dotenv
load_dotenv()

prompt1 = PromptTemplate(
    template="Give a joke about {topic}.", 
    input_variables=["topic"]
)

prompt2 = PromptTemplate(
    template="Generate a explanation for the following joke: {joke}",
    input_variables=["joke"]
)

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

joke_gen_chain = RunnableSequence(prompt1, llm, parser)
parallel_chain = RunnableParallel({
    'joke': RunnablePassthrough(),
    'explanation': RunnableSequence(prompt2, llm, parser)
})

final_chain = RunnableSequence(joke_gen_chain, parallel_chain)

result = final_chain.invoke({"topic": "programming"})
print(result)