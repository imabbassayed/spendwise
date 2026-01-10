def compute_basic_stats(df):
    total = df["amount"].sum()
    monthly_avg = df.groupby(df["date"].dt.to_period("M"))["amount"].sum().mean()
    return float(total), float(monthly_avg)


def compute_monthly_chart(df):
    df["month"] = df["date"].dt.to_period("M").astype(str)
    monthly = df.groupby("month")["amount"].sum()
    return list(monthly.index), list(monthly.values)