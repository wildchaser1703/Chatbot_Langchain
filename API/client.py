import requests
import streamlit as st

def get_openai_response(input_text):
    response = requests.post("http://localhost:5000/haiku_openai",
                             json = {"input": {"topic": input_text}})
    return response.json()["output"]["content"]

def get_ollama_response(input_text):
    response = requests.post(
        "http://localhost:5000/summarize_ollama/invoke",
        json={"input": {"text": input_text}},
    )
    return response.json()["output"]  


st.title("Langchain API Client")

# 1. Selection: Choose the desired operation
operation = st.radio(
    "Choose the operation:",
    ("Write a Haiku (OpenAI)", "Summarize Text (Ollama)")
)

# 2. Input: Get the text from the user
if operation == "Write a Haiku (OpenAI)":
    user_input = st.text_input("Enter the **topic** for the Haiku:", key="haiku_topic")
else: 
    user_input = st.text_area("Enter the **text** you want to summarize:", key="summary_text")


# 3. Execution: Run the model ONLY when the button is clicked
button_clicked = st.button("Generate Response") 

if button_clicked:
    if user_input:
        with st.spinner('Generating response...'):
            if operation == "Write a Haiku (OpenAI)":
                haiku = get_openai_response(user_input)
                st.subheader("Haiku from OpenAI:")
                st.write(haiku)

            elif operation == "Summarize Text (Ollama)":
                summary = get_ollama_response(user_input)
                st.subheader("Summary from Ollama:")
                st.write(summary)
    else:
        st.error("Please provide input text before generating a response.")