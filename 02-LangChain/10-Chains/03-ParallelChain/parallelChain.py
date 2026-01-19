from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel
from dotenv import load_dotenv

load_dotenv()

model1 = ChatOpenAI(model='gpt-4o-mini')
model2 = ChatOpenAI(model='gpt-4o-mini')
model3 = ChatOpenAI(model='gpt-4o-mini')

prompt1 = PromptTemplate(
    template='Generate short and simple notes from the following text: {text}',
    input_variables=['text']
)
prompt2 = PromptTemplate(
    template='Generate 5 short quiz questions answers from following text: {text}',
    input_variables=['text']
)
prompt3 = PromptTemplate(
    template='Merge the notes and quiz into a single document: \nNotes: {notes} \nQuiz: {quiz}',
    input_variables=['notes', 'quiz']
)

parser = StrOutputParser()

runnable_parallel_chain = RunnableParallel({
    'notes': prompt1 | model1 | parser,
    'quiz': prompt2 | model2 | parser,
})
merge_chain = prompt3 | model3 | parser
chain = runnable_parallel_chain | merge_chain

text = 'AI and Quantum Computing'
res = chain.invoke({'text': text})
print(res)

chain.get_graph().print_ascii()