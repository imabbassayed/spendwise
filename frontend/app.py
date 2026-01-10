import streamlit as st
import pandas as pd
import requests
import plotly.express as px


from frontend.components.category_manager import category_manager

API_BASE = "http://127.0.0.1:5000"

st.title("SpendWise")
st.set_page_config(
    page_title="SpendWise",
    page_icon="💰",
)


st.header("Step 1: Set Your Spending Categories")

user_categories = category_manager()

st.divider()

st.header("Step 2: Upload Your Spendings")

# Allow the user to upload a CSV file
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

df = None

if uploaded_file is not None:
    # Show a quick preview of the uploaded data
    df = pd.read_csv(uploaded_file)
    #st.subheader("Local Preview")
    #st.dataframe(df.head())

    # Send the file to the Flask backend for processing
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
    response = requests.post(f"{API_BASE}/upload", files=files)

    # Display the backend response (preview, filename, rows)
    #st.subheader("Backend Response")
    #st.json(response.json())

# Analyize Button
if df is not None:
    col1, col2 = st.columns([6, 1])   # Left wide, right narrow
    with col2:
        analyze_clicked = st.button("Analyze")

    if analyze_clicked:
        with st.spinner("Processing your spending..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}

            # Draw spending line chart
            resp = requests.post(f"{API_BASE}/draw_spending", files=files)

            if resp.status_code != 200:
                st.error("Error analyzing data.")
            else:
                result = resp.json()

                fig = px.line(
                    x=result["months"],
                    y=result["totals"],
                    markers=True,
                    title="Monthly Spending Overview"
                )

                fig.update_xaxes(title_text="Month", type="category")
                fig.update_yaxes(title_text="Spending (USD)")

                st.plotly_chart(fig, use_container_width=True)


st.divider()
st.header("Categorize Spending With AI")

if df is not None:
    col1, col2 = st.columns([6, 1])
    with col2:
        categorize_clicked = st.button("Categorize")

    if categorize_clicked:
        with st.spinner("Categorizing transactions using AI..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            categories_csv = ",".join(user_categories["Category"].tolist())

            resp = requests.post(
                f"{API_BASE}/categorize_spending",
                files=files,
                data={"categories": categories_csv}
            )

            result = resp.json()
            st.json(result)

            if "error" in result:
                st.error(result["error"])
            else:
                st.success("Categorization complete!")

                # --- Pie Chart ---
                summary = result["summary"]
                labels = list(summary.keys())
                values = list(summary.values())

                fig = px.pie(
                    names=labels,
                    values=values,
                    title="Spending Breakdown by Category"
                )
                st.plotly_chart(fig, use_container_width=True)