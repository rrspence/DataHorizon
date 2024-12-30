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
    st.write("Ask me anything about data analysis, visualizations, or debugging Python errors!")

    # Dropdown to select query type
    query_type = st.selectbox("Select the type of query:", ["General Question", "Error Debugging"])

    # Input box for user queries
    if query_type == "General Question":
        user_query = st.text_input("Enter your question about data analysis or visualization:")
    elif query_type == "Error Debugging":
        user_query = st.text_area("Paste the Python error message you want help with:")

    if user_query:  # Check if the user entered a query
        # Show a loading spinner while waiting for the API response
        with st.spinner("Analyzing your query..."):
            try:
                # Set the system message dynamically based on query type
                if query_type == "General Question":
                    system_message = "You are a helpful assistant that specializes in data analysis and visualization."
                    formatted_query = user_query
                elif query_type == "Error Debugging":
                    system_message = "You are a helpful assistant that specializes in debugging Python errors."
                    formatted_query = f"Explain and suggest a fix for this error: {user_query}"

                # Send query to OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": formatted_query}
                    ]
                )
                # Extract and display the response content
                answer = response['choices'][0]['message']['content']
                st.write(answer)
            except Exception as e:
                st.error(f"An error occurred: {e}")
