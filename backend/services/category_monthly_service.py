def category_monthly(df):
    df["month"] = df["date"].dt.to_period("M").astype(str)
    pivot = df.pivot_table(
        index="month",
        columns="category",
        values="amount",
        aggfunc="sum",
        fill_value=0
    )
    return pivot.to_dict()