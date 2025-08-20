# problem statement:
# we have some reviews of a phone in text and pass it to LLM and its gives a structured output giving items - summary, sentiment

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated

load_dotenv()
model = ChatOpenAI(model = 'gpt-4o-mini')

# schema
class ReviewOutput(TypedDict):
    summary: Annotated[str, "A brief summary of the review"]
    sentiment: Annotated[str, "The sentiment of the review: positive, negative, or neutral"]

structured_model = model.with_structured_output(ReviewOutput)

result1 = structured_model.invoke("""The hardware is great, but the softwar feeld bloated. There are too many pre-installed apps that I can't remove. Also, the UI looks outdated compared to other brands. Hoping for a software update to fix this.""")

print(result1)
print(type(result1))

result2 = structured_model.invoke("""The phone is fantastic! The performance is smooth, the camera quality is excellent, and the battery lasts all day. I love the clean user interface and the useful features. Highly recommended!""")

print(result2)
print(type(result2))