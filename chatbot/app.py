from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

# load .env into the environment (if present)
load_dotenv()

# os.getenv can return None, so provide safe string defaults so os.environ always gets a str
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')
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
st.title("LangChain OpenAI Chat Example")
input_text = st.text_input("Enter your question here:")

## OpenAI LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))
