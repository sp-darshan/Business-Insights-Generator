import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate synthetic Superstore sales dataset
np.random.seed(42)

start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)

# Generate date range
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Parameters
n_records = len(dates) * 5  # ~5 transactions per day on average

# Random allocation across date range
random_dates = [dates[np.random.randint(0, len(dates))] for _ in range(n_records)]

# Create dataframe
data = {
    'OrderDate': random_dates,
    'Quantity': np.random.randint(1, 15, n_records),
    'SalesAmount': np.random.uniform(20, 500, n_records).round(2),
    'Profit': np.random.uniform(-50, 200, n_records).round(2),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], n_records),
    'Category': np.random.choice(['Electronics', 'Furniture', 'Clothing', 'Food'], n_records),
    'CustomerID': [f'CUST_{i % 500}' for i in range(n_records)]
}

df = pd.DataFrame(data)
df = df.sort_values('OrderDate').reset_index(drop=True)

# Save to CSV
output_path = 'd:/Projects/College/business_insights_generator/data/superstore_sales.csv'
df.to_csv(output_path, index=False)

print(f"✅ Synthetic dataset created: {output_path}")
print(f"📊 Shape: {df.shape}")
print(f"📅 Date range: {df['OrderDate'].min()} to {df['OrderDate'].max()}")
print(f"\nFirst 5 rows:\n{df.head()}")
