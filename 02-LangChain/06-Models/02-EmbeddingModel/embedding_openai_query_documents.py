from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(
    model='text-embedding-3-small',
    dimensions=10
)

documents = [
    "Delhi is the capital of india",
    "Paris is the capital of france"
]

embeddings = embedding.embed_documents(documents)
print(str(embeddings))