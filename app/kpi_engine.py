def calculate_kpis(df):

    total_revenue = df["TotalPrice"].sum()

    average_order_value = (
        df.groupby("InvoiceNo")["TotalPrice"]
        .sum()
        .mean()
    )

    unique_customers = df["CustomerID"].nunique()

    top_country = (
        df.groupby("Country")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )

    top_product = (
        df.groupby("Description")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )

    return {
        "total_revenue": float(total_revenue),
        "average_order_value": float(average_order_value),
        "unique_customers": int(unique_customers),
        "top_country": top_country,
        "top_product": top_product,
    }
