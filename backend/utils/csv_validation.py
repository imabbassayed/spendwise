import pandas as pd

# Columns required in every uploaded CSV
REQUIRED_COLUMNS = ["date", "merchant", "amount"]

def validate_csv(file):
    """
    Check if the uploaded CSV can be read and has the required columns.
    """
    try:
        df = pd.read_csv(file)
    except Exception:
        return False, "Unable to read CSV."

    # Check for missing columns
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        return False, f"Missing columns: {', '.join(missing)}"

    return True, df