from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv
load_dotenv()

loader = TextLoader(r'D:\Generative AI\Generative AI\02-LangChain\12-RAG\01-DocumentLoaders\01-TextLoader\cricket.txt', encoding='utf-8')
docs = loader.load()

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()
prompt = PromptTemplate(
    template="Summarize the following text: \n{text}",
    input_variables=["text"]
)

chain = prompt | llm | parser
result = chain.invoke({"text": docs[0].page_content})
print(result)