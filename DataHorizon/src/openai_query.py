import streamlit as st # Import Streamlit for the app interface 
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key 
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Make sure it's set in the .env file.")

# Send a query 
response = openai.Completion.create(
    engine="text-davinci-003", # NLP Model
    prompt="What is a scatter plot?",
    max_tokens=100
)