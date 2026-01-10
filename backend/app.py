from flask import Flask, request, jsonify
import pandas as pd

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

    # Allow only CSV files
    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Only CSV files allowed"}), 400

    # Load the CSV into a Pandas DataFrame
    df = pd.read_csv(file)

    # Return first few rows as a quick preview
    preview = df.head().to_dict(orient="records")

    return jsonify({
        "filename": file.filename,
        "rows": len(df),
        "preview": preview
    })