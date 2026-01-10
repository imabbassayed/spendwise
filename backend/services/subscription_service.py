def detect_subscriptions(df):
    df["month"] = df["date"].dt.to_period("M")
    subs = (
        df.groupby(["merchant", "amount"])["month"]
        .nunique()
        .reset_index(name="months")
    )
    subs = subs[subs["months"] >= 2]  # appears 2+ months = possible subscription
    return subs[["amount", "merchant"]].to_dict(orient="records")