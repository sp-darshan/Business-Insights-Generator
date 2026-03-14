import pandas as pd
from app.kpi_engine import calculate_kpis
from app.arima_model import forecast_revenue
from app.monte_carlo import monte_carlo_simulation
from app.data_preprocessor_dynamic import get_monthly_revenue


def run_what_if_analysis(df, country=None, revenue_change_percent=0):

    df_modified = df.copy()

    # Handle both old and new column names
    amount_col = 'Amount' if 'Amount' in df_modified.columns else 'TotalPrice'
    country_col = 'Country' if 'Country' in df_modified.columns else 'Region'

    # Apply revenue change for specific country/region
    if country:
        mask = df_modified[country_col] == country
        df_modified.loc[mask, amount_col] *= (1 + revenue_change_percent / 100)

    # Recalculate monthly revenue
    monthly_revenue = get_monthly_revenue(df_modified, amount_column=amount_col, date_column='Date')

    # Recalculate KPIs
    new_kpis = calculate_kpis(df_modified)

    # Re-run forecast
    new_forecast = forecast_revenue(monthly_revenue)

    # Re-run Monte Carlo
    new_monte_carlo = monte_carlo_simulation(monthly_revenue, new_forecast)

    return {
        "updated_kpis": new_kpis,
        "updated_forecast": new_forecast,
        "updated_monte_carlo": new_monte_carlo
    }