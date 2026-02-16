from fastapi import FastAPI
from app.data_preprocessor import load_and_clean_data, get_monthly_revenue
from app.kpi_engine import calculate_kpis
from app.arima_model import forecast_revenue
from app.insight_engine import generate_summary

app = FastAPI()


@app.get("/generate-insights")
def generate_insights():

    df = load_and_clean_data("data/online_retail.csv")

    monthly_revenue = get_monthly_revenue(df)

    kpis = calculate_kpis(df)

    forecast = forecast_revenue(monthly_revenue)

    summary = generate_summary(kpis, forecast)

    return {
        "kpis": kpis,
        "forecast": forecast,
        "insights": summary
    }
