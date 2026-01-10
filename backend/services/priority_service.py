import pandas as pd
import json

def attach_priorities(df, priority_map_json):
    """Add priority column to df based on category."""
    priority_map = json.loads(priority_map_json)

    df["priority"] = df["category"].map(priority_map).fillna("Unassigned")
    return df


def priority_totals(df):
    """Compute total spending per priority."""
    totals = df.groupby("priority")["amount"].sum().to_dict()
    return totals


def priority_monthly(df):
    """Compute priority spending per month."""
    df["month"] = df["date"].dt.to_period("M").astype(str)
    pivot = df.pivot_table(
        index="month",
        columns="priority",
        values="amount",
        aggfunc="sum",
        fill_value=0
    )

    return pivot.to_dict()