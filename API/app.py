# responsible for creating and running the API server
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv

# load .env into the environment (if present)
load_dotenv()

# Set LangChain tracing and API Key from environment variables
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv('LANGCHAIN_TRACING_V2', 'true')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY', '')

app = FastAPI(
    title = "Langchain Server", 
    version = "1.0.0",
    description = "Simple API server for Langchain models"
)

add_routes(
    app,
    ChatOpenAI(),
    path="/chat_openai"
)

# Initialize models
model = ChatOpenAI()
ollama_model = Ollama(model="qwen2.5-coder:0.5b")

# Define prompts
prompt1 = ChatPromptTemplate.from_template("Write a haiku about {topic}.")
prompt2 = ChatPromptTemplate.from_template("Summarize the following text in one sentence: {text}")

# Add routes for the chains
add_routes(
    app,
    prompt1 | model,
    path="/haiku_openai" 
)

add_routes(
    app,
    prompt2 | ollama_model,
    path="/summarize_ollama"
)

if __name__ == "__main__":
    # Ensure uvicorn is running on the port expected by the client (5000)
    uvicorn.run(app, host="localhost", port=5000)