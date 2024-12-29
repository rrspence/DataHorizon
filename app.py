
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Challenge Generator 
st.title("DataHorizon Practice Mode")
st.sidebar.header("Practice Categories")
categories = ["Filtering", "Transformations", "Visualizations"]
selected_category = st.sidebar.selectbox("Select Practice Category", categories)

# Challenge Generator: Filtering
if selected_category == "Filtering":
    st.header("Filtering Challenge")
    st.write("Challenge: Filter the dataset to show rows where `column_name` is greater than 50.")

    # Load example dataset
    data = {"column_name": [10, 60, 45, 90, 55], "other_column": [100, 200, 300, 400, 500]}
    df = pd.DataFrame(data)
    st.write("Dataset:")
    st.dataframe(df)

    # User Input for Code
    user_code = st.text_area("Write your filtering code here (e.g., `df[df['column_name'] > 50`]):", height=100) 

    # Submission and Evaluation
    if st.button("Submit"):
        try: 
            filtered_df = eval(user_code)
            st.write("Your Result:")
            st.dataframe(filtered_df)

            # Grading
            expected_df = df[df["column_name"] > 50]
            if filtered_df.equals(expected_df):
                st.success("Correct! Great Job!")
            else:
                st.error("Not quite. Check your filter condition and try again.")
        except Exception as e:
            st.error(f"Error in your code: {e}")