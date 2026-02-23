# convert any python function into a runnable
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnablePassthrough, RunnableParallel, RunnableLambda
from dotenv import load_dotenv
load_dotenv()

def word_count(text: str) -> int:
    return len(text.split())

prompt = PromptTemplate(
    template="Generate a joke about {topic}.",
    input_variables=["topic"],
)

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

runnable_word_count_chain = RunnableLambda(word_count)
sequence_chain = RunnableSequence(prompt, llm, parser)
parallel_chain = RunnableParallel({
    "joke_word_count": runnable_word_count_chain,
    "joke": RunnablePassthrough()
})

chain = RunnableSequence(sequence_chain, parallel_chain)
print(chain.invoke({"topic": "programming"}))