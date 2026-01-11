import pandas as pd
import io
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.csv_validation import validate_csv

def test_valid_csv():
    # Build a valid CSV in memory
    csv_content = "date,merchant,amount\n2025-01-01,Walmart,50.0\n"
    fake_file = io.StringIO(csv_content)

    is_valid, result = validate_csv(fake_file)

    assert is_valid is True
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["date", "merchant", "amount"]