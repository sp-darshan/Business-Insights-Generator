import pandas as pd


def load_and_clean_data(file_path: str):
    df = pd.read_csv(file_path)

    # Convert to datetime
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], dayfirst=True)

    # Remove cancelled invoices
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

    # Remove negative quantities
    df = df[df["Quantity"] > 0]

    # Create TotalPrice
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    return df


def get_monthly_revenue(df):
    monthly_revenue = df.resample("ME", on="InvoiceDate")["TotalPrice"].sum()

    return monthly_revenue

def get_daily_revenue(df):
    daily_revenue = df.resample("D", on="InvoiceDate")["TotalPrice"].sum()
    return daily_revenue
