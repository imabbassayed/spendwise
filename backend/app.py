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