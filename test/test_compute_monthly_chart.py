import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.services.analysis_service import compute_monthly_chart

def test_compute_monthly_chart():
    df = pd.DataFrame({
        "date": pd.to_datetime([
            "2025-01-02", "2025-01-15",
            "2025-02-01"
        ]),
        "amount": [50, 100, 200]
    })

    months, totals = compute_monthly_chart(df)

    assert months == ["2025-01", "2025-02"]
    assert totals == [150, 200]

    assert isinstance(months, list)
    assert isinstance(totals, list)