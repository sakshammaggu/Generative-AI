from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.header('Research Tool')
model = ChatOpenAI(model = 'gpt-4o-mini')
user_input = st.text_input('Enter your prompt')

if (st.button('Summarize')):
    result = model.invoke(user_input)
    st.write(result.content)