from flask import Flask, request, jsonify
import pandas as pd

from utils.csv_validation import validate_csv
app = Flask(__name__)

@app.route("/health")
def health():
    # Endpoint to confirm the server is running
    return jsonify({"status": "ok"})


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

    # Return first few rows as a preview
    preview = df.head().to_dict(orient="records")

    return jsonify({
        "filename": file.filename,
        "rows": len(df),
        "preview": preview
    })


@app.route("/draw_spending", methods=["POST"])
def draw_spending():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    df = pd.read_csv(file)

    required = ["date", "description", "amount"]
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
