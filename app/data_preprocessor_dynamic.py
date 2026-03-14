import pandas as pd
from typing import Dict, List
import os


def load_and_clean_data_dynamic(
    file_path: str,
    column_mapping: Dict[str, str],
    date_format: str = None
):
    """
    Load and clean data with dynamic column mapping.
    
    Args:
        file_path: Path to CSV file
        column_mapping: Dict mapping standard names to actual column names
            Required keys: 'date_column', 'amount_column'
            Optional: 'quantity_column', 'country_column'
        date_format: Optional date format string (e.g., '%d-%m-%Y')
    
    Returns:
        DataFrame with standardized columns
    """
    # Read CSV with error handling for malformed rows
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip', engine='python')
    except Exception:
        # Fallback to default CSV reading
        df = pd.read_csv(file_path, on_bad_lines='skip')
    
    # Extract mapped column names
    date_col = column_mapping.get('date_column')
    amount_col = column_mapping.get('amount_column')
    quantity_col = column_mapping.get('quantity_column')
    country_col = column_mapping.get('country_column')
    
    # Validate required columns exist
    if date_col not in df.columns:
        raise ValueError(f"Date column '{date_col}' not found in dataset")
    if amount_col not in df.columns:
        raise ValueError(f"Amount column '{amount_col}' not found in dataset")
    
    # Standardize column names
    df = df.rename(columns={
        date_col: 'Date',
        amount_col: 'Amount',
        quantity_col: 'Quantity' if quantity_col else None,
        country_col: 'Country' if country_col else None
    })
    
    # Remove None columns from rename
    df = df.dropna(axis=1, how='all')
    
    # Convert Date column to datetime with intelligent parsing
    try:
        if date_format:
            # Try the specific format first
            try:
                df['Date'] = pd.to_datetime(df['Date'], format=date_format)
            except Exception:
                # If specific format fails, try auto-detection with dayfirst=True
                # This handles DD-MM-YYYY formats correctly
                df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
                if df['Date'].isna().all():
                    raise ValueError(f"Could not parse date column with format {date_format} or auto-detection")
        else:
            # Auto-detect with dayfirst=True for non-US date formats
            df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
            if df['Date'].isna().all():
                # Try without dayfirst if all failed
                df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True, errors='coerce')
            if df['Date'].isna().all():
                raise ValueError("Could not parse date column: all dates failed to parse")
    except Exception as e:
        raise ValueError(f"Could not parse date column: {str(e)}")
    
    # Clean Amount column (ensure numeric)
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    
    # Remove rows with missing critical values
    df = df.dropna(subset=['Date', 'Amount'])
    
    # Remove negative amounts if quantity-based
    if 'Quantity' in df.columns:
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df = df[df['Quantity'] > 0]
    
    df = df[df['Amount'] > 0]
    
    return df.sort_values('Date').reset_index(drop=True)


def get_monthly_revenue(df, amount_column: str = 'Amount', date_column: str = 'Date'):
    """Generate monthly revenue from cleaned data"""
    # Ensure we have a copy to avoid modifying original
    df_copy = df.copy()
    df_copy = df_copy.set_index(date_column)
    monthly_revenue = (
        df_copy[amount_column]
        .resample("ME")
        .sum()
        .sort_index()
    )
    return monthly_revenue


def get_daily_revenue(df, amount_column: str = 'Amount', date_column: str = 'Date'):
    """Generate daily revenue from cleaned data"""
    # Ensure we have a copy to avoid modifying original
    df_copy = df.copy()
    df_copy = df_copy.set_index(date_column)
    daily_revenue = df_copy[amount_column].resample("D").sum()
    return daily_revenue


def get_dataset_info(df):
    """Get basic info about the dataset"""
    return {
        'total_records': len(df),
        'date_range': {
            'start': str(df['Date'].min()),
            'end': str(df['Date'].max())
        },
        'columns': list(df.columns),
        'shape': list(df.shape),
        'total_amount': float(df['Amount'].sum()),
        'average_transaction': float(df['Amount'].mean())
    }
