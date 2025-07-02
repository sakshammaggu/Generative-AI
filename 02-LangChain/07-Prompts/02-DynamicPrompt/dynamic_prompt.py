from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import streamlit as st

load_dotenv()

st.header('Research Tool')
model = ChatOpenAI(model = 'gpt-4o-mini')

paper_input = st.selectbox('Select a paper', ["Select...", "Attention is all you need", "BERT", "GPT-3", "Diffusion model beat GANs on image synthesis"])

style_input = st.selectbox('Select explanation style:', ["Explain like I'm a genius", "Explain like I'm a professor", "Explain like I'm a student", "Mathematical", "Code-Oriented"])

length_input = st.selectbox('Select explanationlength:', ["Short", "Medium", "Long"])

prompt_template = PromptTemplate(
    template = """
        Please summarize the research paper titled "{paper_input}" with the following specifications: Explanation Style: {style_input} 
        Explanation Length: {length_input}  
        1. Mathematical Details:
            - Include relevant mathematical equations if present in the paper. 
            - Explain the mathematical concepts using simple, intuitive code snippets where applicable. 
        2. Analogies:     
            - Use relatable analogies to simplify complex ideas. 
            - If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.  
        Ensure the summary is clear, accurate, and aligned with the provided style and length.
        You are a helpful assistant that explains research papers in a way that is easy to understand.
    """,
    input_variables = ["paper_input", "style_input", "length_input"]
)

prompt = prompt_template.invoke({
    'paper_input': paper_input,
    'style_input': style_input,
    'length_input':length_input
})

if (st.button('Summarize')):
    result = model.invoke(prompt)
    st.write(result.content)