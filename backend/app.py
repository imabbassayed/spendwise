from flask import Flask, request, jsonify
from openai import OpenAI
import pandas as pd
import sys
import os

# Add root directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import config


from utils.csv_validation import validate_csv
from services.analysis_service import compute_basic_stats, compute_monthly_chart

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

    

   

    # Build final response
    return jsonify({
        "total_spending": total,
        "avg_monthly": avg,
        "monthly_chart": {"months": months, "totals": totals},
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


client = OpenAI(api_key=config.OPENAI_API_KEY)

SYSTEM_PROMPT = config.SYSTEM_PROMPT_CATEGORIZER

@app.route("/categorize_spending", methods=["POST"])
def categorize_spending():
    # Validate input
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    if "categories" not in request.form:
        return jsonify({"error": "No category list provided"}), 400

    # Clean categories
    categories = [c.strip() for c in request.form["categories"].split(",")]

    # Read CSV
    file = request.files["file"]
    file.seek(0)
    df = pd.read_csv(file)

    # Validate required columns
    for col in ["date", "merchant", "amount"]:
        if col not in df.columns:
            return jsonify({"error": f"Missing column: {col}"}), 400

    df["category"] = ""

  

    # Process each merchant
    for idx, row in df.iterrows():
        merchant = str(row["merchant"])

        prompt = f"""
        Merchant: "{merchant}"
        Allowed categories: {categories}
        Respond with ONLY the exact category name.
        """

        try:
            response = client.chat.completions.create(
                model=config.MODEL_NAME_CATEGORIZER,
                temperature=0,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            )

            pred = response.choices[0].message.content.strip()


            # Validate model output
            if pred not in categories:
                pred = "Other" if "Other" in categories else categories[0]

            df.at[idx, "category"] = pred

        except Exception as e:
            print("❌ OpenAI Error:", e)
            df.at[idx, "category"] = "Other" if "Other" in categories else categories[0]


    # Summary for pie chart
    summary = df.groupby("category")["amount"].sum().to_dict()

    categorized_list = df[["merchant", "amount", "category"]].to_dict(orient="records")

    return jsonify({
        "categorized": categorized_list,
        "summary": summary
    })