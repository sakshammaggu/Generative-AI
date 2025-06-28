from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(
    model='text-embedding-3-small',
    dimensions=10
)

embeddings = embedding.embed_query("Delhi is the capital of india")
print(str(embeddings))