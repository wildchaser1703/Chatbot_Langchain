from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import streamlit as st
import os
from dotenv import load_dotenv

# load .env into the environment (if present)
load_dotenv()

# os.getenv can return None, so provide safe string defaults so os.environ always gets a str
## Langsmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv('LANGCHAIN_TRACING_V2', 'true')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY', '')

## Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that responds to user queries."),
        ("user", "Question: {question}")
    ]
)

## Streamlit framework
st.title("LangChain Ollama Chat Example")
input_text = st.text_input("Enter your question here:")

## Ollama LLM
llm = Ollama(model="qwen2.5-coder:0.5b", temperature=0)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))
