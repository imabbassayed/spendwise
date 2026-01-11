import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.services.analysis_service import compute_basic_stats

def test_compute_basic_stats():
    df = pd.DataFrame({
        "date": pd.to_datetime([
            "2025-01-02", "2025-01-15",  # January: total = 150
            "2025-02-01"                 # February: total = 200
        ]),
        "amount": [50, 100, 200]
    })

    total, monthly_avg = compute_basic_stats(df)

    assert isinstance(total, float)
    assert isinstance(monthly_avg, float)

    assert total == 350.0          # 50 + 100 + 200
    assert monthly_avg == 175.0    # (150 + 200) / 2