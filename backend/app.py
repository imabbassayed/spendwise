from flask import Flask, request, jsonify
import pandas as pd

from utils.csv_validation import validate_csv
from services.analysis_service import compute_basic_stats, compute_monthly_chart
from services.subscription_service import detect_subscriptions
from services.categorization_service import categorize_transactions
from services.category_monthly_service import category_monthly
from services.priority_service import attach_priorities, priority_totals, priority_monthly
from services.anomaly_service import detect_category_anomalies

app = Flask(__name__)

@app.route("/health")
def health():
    # Basic endpoint to confirm the server is running
    return jsonify({"status": "ok"})




@app.route("/analyze", methods=["POST"])
def analyze():
    # Validate file exists
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    if "categories" not in request.form:
        return jsonify({"error": "No category list provided"}), 400


    file = request.files["file"]

    # Validate CSV structure
    valid, result = validate_csv(file)
    if not valid:
        return jsonify({"error": result}), 400

    df = result
    df["date"] = pd.to_datetime(df["date"])

  

    # Compute top-level financial stats
    total, avg = compute_basic_stats(df)

    # Compute monthly spending chart
    months, totals = compute_monthly_chart(df)

    # Detect recurring subscription-like charges
    subscriptions = detect_subscriptions(df)

    # Read user-defined categories
    categories = request.form["categories"].split(",")

    # Categorize each merchant using OpenAI
    df = categorize_transactions(df, categories)

    # Compute category totals
    category_spend = df.groupby("category")["amount"].sum().to_dict()

    # Compute category spending by month
    category_month_data = category_monthly(df)

    # Attach priority levels to each categorized transaction
    df = attach_priorities(df, request.form["priority_map"])

    # Compute spending totals by priority
    priority_spend = priority_totals(df)

    # Compute month × priority spending
    priority_month_data = priority_monthly(df)

    # Detect anomalies in category spending
    anomalies = detect_category_anomalies(df)



    

   

    # Build final response
    return jsonify({
        "total_spending": total,
        "avg_monthly": avg,
        "monthly_chart": {"months": months, "totals": totals},
        "subscriptions": subscriptions,
        "category_spending": category_spend,
        "category_monthly": category_month_data,
        "priority_spending": priority_spend,
        "priority_monthly": priority_month_data,
        "anomalies": anomalies,
        "categorized": df.to_dict(orient="records")
    })


