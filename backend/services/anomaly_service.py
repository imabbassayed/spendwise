import sys
import os
# Add root directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config
import pandas as pd

def detect_category_anomalies(df):    
    
    # Detects anomalies in category spending per month using Z-score.
    z_threshold = config.ANAMOLY_DETECTION_Z_THRESHOLD

    df["month"] = df["date"].dt.to_period("M").astype(str)

    # Compute month totals per category
    pivot = df.pivot_table(
        index="month",
        columns="category",
        values="amount",
        aggfunc="sum",
        fill_value=0
    )

    anomalies = {}

    for category in pivot.columns:
        values = pivot[category]

        mean = values.mean()
        std = values.std()

        # Avoid divide-by-zero
        if std == 0:
            continue

        z_scores = (values - mean) / std

        outliers = z_scores[abs(z_scores) > z_threshold]

        if len(outliers) > 0:
            anomalies[category] = [
                {
                    "month": month,
                    "amount": float(values.loc[month]),
                    "z_score": float(z_scores.loc[month])
                }
                for month in outliers.index
            ]

    return anomalies