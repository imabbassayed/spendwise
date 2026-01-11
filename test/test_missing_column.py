import pandas as pd
import io
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.utils.csv_validation import validate_csv

def test_missing_column():
    # CSV missing the 'date' column
    csv_content = "merchant,amount\nWalmart,50.0\n"
    fake_file = io.StringIO(csv_content)

    is_valid, msg = validate_csv(fake_file)

    assert is_valid is False
    assert "Missing columns" in msg
    assert "date" in msg
