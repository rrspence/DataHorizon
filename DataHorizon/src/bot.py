import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API key not found. Make sure it's set in the .env file.")
    st.stop()

# Set OpenAI API key
openai.api_key = api_key

# Bot Interaction Section
def bot_section():
    st.title("DataHorizon Bot")
    st.write("Ask me anything about data analysis or visualizations!")

    # Input box for user queries
    user_query = st.text_input("Your Question:")

    if user_query:  # Check if the user entered a question
        # Show a loading spinner while waiting for the API response
        with st.spinner("Generating response..."):
            try:
                # Send query to OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant specialized in data analysis and visualization."},
                        {"role": "user", "content": user_query}
                    ]
                )
                # Extract and display the response content
                answer = response['choices'][0]['message']['content']
                st.write(answer)
            except Exception as e:
                st.error(f"An error occurred: {e}")
