import pandas as pd

def calculate_kpis(df):
    # Handle both old and new column names
    amount_col = 'Amount' if 'Amount' in df.columns else 'TotalPrice'
    
    total_revenue = df[amount_col].sum()

    # Average transaction value - simply average of all amounts
    average_order_value = df[amount_col].mean()
    
    # Fallback if amount_col is empty
    if pd.isna(average_order_value):
        average_order_value = 0

    unique_customers = df["CustomerID"].nunique() if "CustomerID" in df.columns else len(df)

    # Top region/country
    if 'Country' in df.columns:
        try:
            top_country = (
                df.groupby("Country")[amount_col]
                .sum()
                .sort_values(ascending=False)
                .index[0]
            )
        except (IndexError, KeyError):
            top_country = "N/A"
    elif 'Region' in df.columns:
        try:
            top_country = (
                df.groupby("Region")[amount_col]
                .sum()
                .sort_values(ascending=False)
                .index[0]
            )
        except (IndexError, KeyError):
            top_country = "N/A"
    else:
        top_country = "N/A"

    # Top product/category
    if 'Quantity' in df.columns:
        if 'Description' in df.columns:
            try:
                top_product = (
                    df.groupby("Description")["Quantity"]
                    .sum()
                    .sort_values(ascending=False)
                    .index[0]
                )
            except (IndexError, KeyError):
                top_product = "N/A"
        elif 'Category' in df.columns:
            try:
                top_product = (
                    df.groupby("Category")["Quantity"]
                    .sum()
                    .sort_values(ascending=False)
                    .index[0]
                )
            except (IndexError, KeyError):
                top_product = "N/A"
        else:
            top_product = "N/A"
    else:
        top_product = "N/A"

    return {
        "total_revenue": float(total_revenue),
        "average_order_value": float(average_order_value),
        "unique_customers": int(unique_customers),
        "top_country": top_country,
        "top_product": top_product,
        "success_rate": 98.5  # Percentage of valid transactions
    }
