import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import json

from components.category_manager import category_manager

API_BASE = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="SpendWise",
    page_icon="💰",
)



st.title("💰 SpendWise")
st.markdown("""
Your personal AI-powered financial assistant — helping you understand where your money goes,
spot patterns in your spending, and gain control over your financial habits with clear,
intuitive insights.
""")


st.subheader("🔧 Set Your Categories")
st.caption("Define the categories that matter to you — we'll use them to classify your transactions.")

user_categories = category_manager()


st.subheader("📤 Upload Your Transactions")
st.caption("Upload a CSV file containing your transaction history (date, merchant, amount).")


# Allow the user to upload a CSV file
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])


st.subheader("🎯 Set Your Monthly Savings Goal")
goal_amount = st.number_input(
    "How much do you want to save this month? (USD)",
    min_value=10.0,
    value=300.0,
    step=10.0
)

df = None

if uploaded_file is not None:
    # Load the CSV file
    df = pd.read_csv(uploaded_file)

 
# Analyize Button
if df is not None:
    st.divider()

    col1, col2 = st.columns([6, 1])   # Left wide, right narrow
    with col2:
        analyze_clicked = st.button("Analyze")

    if analyze_clicked:
        with st.spinner("Processing your spending..."):
            st.session_state.goal_amount = goal_amount
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            categories_csv = ",".join(user_categories["Category"].tolist())
            priority_map = user_categories.set_index("Category")["Priority"].to_dict()

            # Draw spending line chart
            resp = requests.post(f"{API_BASE}/analyze", files=files, data={"categories": categories_csv, "priority_map": json.dumps(priority_map), "goal_amount": goal_amount})
                        
            if resp.status_code != 200:
                st.error("Error analyzing data.")
            else:
                st.divider()
                st.header("📝 Analysis Results")
                result = resp.json()


                # Display basic spending metrics to give a quick overview
                st.subheader("1. Spending Overview")
                col1, col2 = st.columns(2)
                col1.metric("Total Spending", f"${result['total_spending']}")
                col2.metric("Average Monthly Spending", f"${result['avg_monthly']}")

                # Plot the monthly spending trend to show changes over time
                st.subheader("2. Monthly Spending Trend")
                fig = px.line(
                    x=result["monthly_chart"]["months"],
                    y=result["monthly_chart"]["totals"],
                    markers=True,
                )
                fig.update_xaxes(title_text="Month", type="category")
                fig.update_yaxes(title_text="Spending (USD)")
                st.plotly_chart(fig, use_container_width=True)

                # List recurring transactions that look like subscriptions
                st.subheader("3.  Subscriptions")

                subs = result["subscriptions"]
                if len(subs) == 0:
                    st.caption("No recurring transactions detected.")
                else:                
                    st.dataframe(result["subscriptions"], use_container_width=True)

                st.warning("Sections 4–7 rely on OpenAI. If the API cannot be reached, SpendWise  will randomly assign categories to your transactions.")

                
                # Show how much was spent in each category after AI classification
                st.subheader("4. Spending by Category ")
                st.bar_chart(result["category_spending"])

                labels = list(result["category_spending"].keys())
                values = list(result["category_spending"].values())

                fig = px.pie(
                    names=labels,
                    values=values,
                )
                st.plotly_chart(fig, use_container_width=True)



                # Present spending broken down per category for each month
                st.subheader("5. Category Spending by Month")
                st.dataframe(result["category_monthly"], use_container_width=True)

                st.subheader("6. Spending by Priority")

                # Bar chart
                st.bar_chart(result["priority_spending"])

                # Pie chart
                labels = list(result["priority_spending"].keys())
                values = list(result["priority_spending"].values())

                fig = px.pie(names=labels, values=values)
                st.plotly_chart(fig, use_container_width=True)

                # Monthly priority spending table

                st.subheader("7. Priority Spending by Month")
                st.dataframe(result["priority_monthly"], use_container_width=True)

                # Highlight any anomalies detected in category spending

                st.subheader("8. Spending Anomalies")

                if len(result["anomalies"]) == 0:
                    st.caption("No significant anomalies detected.")
                else:
                    for category, anomaly_list in result["anomalies"].items():
                        st.markdown(f"#### ⚠️ {category} Anomalies")
                        for a in anomaly_list:
                            st.write(
                                f"- **{a['month']}**: Spent **${a['amount']}**, "
                                f"Z-score = `{a['z_score']:.2f}` (unusual change)"
                    )
                
                # Generate and show personalized savings recommendations
                st.header("9. Savings Strategy Recommendation")
                st.markdown(result["recommendation"])   