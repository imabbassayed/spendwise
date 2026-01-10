from flask import Flask, request, jsonify
import pandas as pd

from utils.csv_validation import validate_csv
from services.analysis_service import compute_basic_stats, compute_monthly_chart
from services.subscription_service import detect_subscriptions
from services.categorization_service import categorize_transactions

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

    file = request.files["file"]

    # Validate CSV structure
    valid, result = validate_csv(file)
    if not valid:
        return jsonify({"error": result}), 400

    df = result
    df["date"] = pd.to_datetime(df["date"])

  

    # Compute top-level financial stats
    total, avg = compute_basic_stats(df)
    print("Total:", total, "Avg:", avg)

    # Compute monthly spending chart
    months, totals = compute_monthly_chart(df)

    # Detect recurring subscription-like charges
    subscriptions = detect_subscriptions(df)
    print("Subscriptions:", subscriptions)

    # Read user-defined categories
    categories = request.form["categories"].split(",")

    # Categorize each merchant using OpenAI
    df = categorize_transactions(df, categories)

    # Compute category totals
    category_spend = df.groupby("category")["amount"].sum().to_dict()

    # Compute category spending by month
    category_month_data = category_monthly(df)
    

   

    # Build final response
    return jsonify({
        "total_spending": total,
        "avg_monthly": avg,
        "monthly_chart": {"months": months, "totals": totals},
        "subscriptions": subscriptions,
        "category_spending": category_spend,
    })


@app.route("/draw_spending", methods=["POST"])
def draw_spending():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    df = pd.read_csv(file)

    required = ["date", "merchant", "amount"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        return jsonify({"error": f"Missing columns: {missing}"}), 400

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["month"] = df["date"].dt.to_period("M")
    df["month_label"] = df["month"].dt.strftime("%b %Y")

    monthly = df.groupby("month_label")["amount"].sum().reset_index()

    # ensure correct order
    monthly = monthly.sort_values("month_label")

    return jsonify({
        "months": monthly["month_label"].tolist(),
        "totals": monthly["amount"].tolist()
    })


@app.route("/upload", methods=["POST"])
def upload_csv():
    # Ensure a file was included in the request
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]


    # CSV validation & required columns check
    valid, result = validate_csv(file)
    if not valid:
        return jsonify({"error": result}), 400
    
    df = result  # validated DataFrame

    # Return first few rows as preview
    preview = df.head().to_dict(orient="records")

    return jsonify({
        "filename": file.filename,
        "rows": len(df),
        "preview": preview
    })