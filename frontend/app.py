import streamlit as st
import pandas as pd
import requests
import plotly.express as px


from components.categories import categories

API_BASE = "http://127.0.0.1:5000"

st.title("SpendWise")
st.set_page_config(
    page_title="SpendWise",
    page_icon="💰",
)


st.header("Step 1: Set Your Spending Categories")

user_categories = categories()




st.divider()

# Allow the user to upload a CSV file
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    # Show a quick preview of the uploaded data
    df = pd.read_csv(uploaded_file)
    st.subheader("Local Preview")
    st.dataframe(df.head())

    # Send the file to the Flask backend for processing
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
    response = requests.post(f"{API_BASE}/upload", files=files)

    # Display the backend response (preview, filename, rows)
    st.subheader("Backend Response")
    st.json(response.json())