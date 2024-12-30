import streamlit as st # Import Streamlit for the app interface 

# Define a dictionary of bot responses
responses = {
    "scatter plot": "A scatter plot displays data points on a two-dimensional plane, typically to show relationships between two variables. Use plt.scatter(x, y).",
    "filter data": "To filter data in a DataFrame, use conditional indexing, e.g., df[df['column'] > value].",
    "bar chart": "A bar chart displays data using rectangular bars. Use plt.bar(x, height).",
}


# Bot Interaction Section
def bot_section():
    st.title("DataHorizon Bot")  # Add a title to the bot section
    st.write("Ask me anything about data analysis or visualizations!")  # Brief description

    # Input box for user queries
    user_query = st.text_input("Your Question:")

    if user_query:  # Check if the user entered a question
        # Normalize the input: strip whitespace and convert to lowercase
        normalized_query = user_query.strip().lower()

        # Match user input to predefined responses
        response = responses.get(
            normalized_query,  # Use the normalized input
            "I'm sorry, I don't have an answer for that yet. Please try asking something else!",
        )
        st.write(response)  # Display the bot's response


