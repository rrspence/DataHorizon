import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from bot import bot_section # Import the bot functionality 

# Question Pool for Practice Mode
question_pool = [
    {
        "category": "Filtering",
        "difficulty": "easy",
        "description": "Filter the dataset to show rows where `column_name` is greater than 50.",
        "dataset": pd.DataFrame({"column_name": [10, 60, 45, 90, 55]}),
        "expected_output": lambda df: df[df["column_name"] > 50]
    },
    {
        "category": "Filtering",
        "difficulty": "medium",
        "description": "Filter the dataset to show rows where `column_name` is greater than 50 and `other_column` is less than 400.",
        "dataset": pd.DataFrame({
            "column_name": [10, 60, 45, 90, 55],
            "other_column": [100, 200, 300, 400, 500]
        }),
        "expected_output": lambda df: df[(df["column_name"] > 50) & (df["other_column"] < 400)]
    },
    {
        "category": "Transformations",
        "difficulty": "easy",
        "description": "Add a new column called `double_column` that is twice the value of `column_name`.",
        "dataset": pd.DataFrame({"column_name": [10, 20, 30]}),
        "expected_output": lambda df: df.assign(double_column=df["column_name"] * 2)
    },
    {
        "category": "Visualizations",
        "difficulty": "medium",
        "description": "Create a bar chart showing the sum of `column_name` grouped by `group_column`.",
        "dataset": pd.DataFrame({
            "column_name": [10, 20, 30],
            "group_column": ["A", "B", "A"]
        }),
        "expected_output": "visualization"
    }
]

# Random Question Selector for Practice Mode
def get_random_question(category=None, difficulty=None):
    filtered_pool = [q for q in question_pool if 
                     (category is None or q["category"] == category) and 
                     (difficulty is None or q["difficulty"] == difficulty)]
    return random.choice(filtered_pool) if filtered_pool else None

# Dashboard Section
def dashboard():
    st.title("DataHorizon Dashboard")

    # File Upload Section
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.header("Filters")

        # Filter Panel
        st.sidebar.subheader("Apply Filters")
        num_filters = st.sidebar.slider("How many filters?", 1, 5, 1)
        filtered_df = df.copy()

        for i in range(num_filters):
            column = st.sidebar.selectbox(f"Filter {i + 1} - Column", df.columns, key=f"filter_col_{i}")
            if df[column].dtype in ["int64", "float64"]:
                min_val, max_val = st.sidebar.slider(
                    f"Filter {i + 1} - Range for {column}",
                    float(df[column].min()),
                    float(df[column].max()),
                    (float(df[column].min()), float(df[column].max())),
                    key=f"filter_range_{i}"
                )
                filtered_df = filtered_df[(filtered_df[column] >= min_val) & (filtered_df[column] <= max_val)]
            else:
                unique_values = df[column].dropna().unique()
                selected_value = st.sidebar.selectbox(f"Filter {i + 1} - Value for {column}", unique_values, key=f"filter_value_{i}")
                filtered_df = filtered_df[filtered_df[column] == selected_value]

        st.header("Filtered Dataset")
        st.dataframe(filtered_df)

        # Visualization Panel
        st.header("Create Visualizations")
        chart_type = st.selectbox("Select Chart Type", ["Bar", "Line", "Scatter"])
        x_axis = st.selectbox("Select X-axis", filtered_df.columns)
        y_axis = st.selectbox("Select Y-axis", filtered_df.columns)

        if st.button("Generate Chart"):
            plt.figure(figsize=(10, 5))
            if chart_type == "Bar":
                filtered_df.groupby(x_axis)[y_axis].sum().plot(kind="bar")
            elif chart_type == "Line":
                plt.plot(filtered_df[x_axis], filtered_df[y_axis])
            elif chart_type == "Scatter":
                plt.scatter(filtered_df[x_axis], filtered_df[y_axis])

            plt.title(f"{chart_type} Chart")
            plt.xlabel(x_axis)
            plt.ylabel(y_axis)
            st.pyplot(plt)

        # Summary Panel
        st.header("Dataset Summary")
        st.write(filtered_df.describe())

        # Export Panel
        st.header("Export Options")
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Filtered CSV", csv, "filtered_dataset.csv", "text/csv")

        if st.button("Save Chart as Image"):
            plt.savefig("chart.png")
            with open("chart.png", "rb") as file:
                st.download_button("Download Chart", file, "chart.png", "image/png")
    else:
        st.info("Please upload a CSV file to start.")

# Practice Mode Section
def practice_mode():
    st.title("Practice Mode")

    # Select Category and Difficulty
    category = st.sidebar.selectbox("Select Category", ["All", "Filtering", "Transformations", "Visualizations"])
    difficulty = st.sidebar.selectbox("Select Difficulty", ["All", "easy", "medium", "hard"])

    # Map to filter function
    selected_category = None if category == "All" else category
    selected_difficulty = None if difficulty == "All" else difficulty

    # Get a random question
    question = get_random_question(selected_category, selected_difficulty)
    if question:
        st.header(question["description"])
        st.write("Dataset:")
        st.dataframe(question["dataset"])

        # User Input
        user_code = st.text_area("Write your code here:")
        if st.button("Submit"):
            try:
                # Evaluate the user's code
                user_result = eval(user_code, {"df": question["dataset"]})

                # Check if the output matches the expected output
                if question["expected_output"] != "visualization":
                    expected_result = question["expected_output"](question["dataset"])
                    if user_result.equals(expected_result):
                        st.success("Correct! Great job!")
                    else:
                        st.error("Not quite. Check your logic and try again.")
                else:
                    st.info("Visualization tasks are not graded automatically yet.")
            except Exception as e:
                st.error(f"Error in your code: {e}")
    else:
        st.write("No questions available for the selected category and difficulty.")

# Sidebar Navigation
def main():
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Go to", ["Dashboard", "Practice Mode"])

    if app_mode == "Dashboard":
        dashboard()
    elif app_mode == "Practice Mode":
        practice_mode()
    elif app_mode == "Bot":
        bot_section() #Display the bot section

if __name__ == "__main__":
    main()
