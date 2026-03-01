from fastapi import FastAPI
from app.data_preprocessor import load_and_clean_data, get_monthly_revenue, get_daily_revenue
from app.kpi_engine import calculate_kpis
from app.arima_model import forecast_revenue
from app.insight_engine import generate_summary
from app.autoencoder import detect_anomalies
from app.vae import generate_scenarios
from app.gan_model import generate_synthetic_data
from app.monte_carlo import monte_carlo_simulation
from fastapi import Body
from app.simulation_engine import run_what_if_analysis

app = FastAPI()

@app.get("/generate-insights")
def generate_insights():

    df = load_and_clean_data("data/online_retail.csv")

    monthly_revenue = get_monthly_revenue(df)

    kpis = calculate_kpis(df)

    forecast = forecast_revenue(monthly_revenue)
    monte_carlo = monte_carlo_simulation(monthly_revenue, forecast)

    summary = generate_summary(kpis, forecast)

    daily_revenue = get_daily_revenue(df)
    risk_analysis = detect_anomalies(daily_revenue)

    scenarios = generate_scenarios(monthly_revenue)
    synthetic_data = generate_synthetic_data(monthly_revenue)

    return {
        "kpis": kpis,
        "forecast": forecast,
        "risk_analysis": risk_analysis,
        "scenarios": scenarios,
        "synthetic_data": synthetic_data,
        "monte_carlo": monte_carlo,
        "insights": summary,
        "meta": {
            "model": "Hybrid GenAI Business Engine v1.0"
        }
    }

@app.post("/what-if")
def what_if_analysis(
    country: str = Body(None),
    revenue_change_percent: float = Body(0)
):

    df = load_and_clean_data("data/online_retail.csv")

    result = run_what_if_analysis(
        df,
        country=country,
        revenue_change_percent=revenue_change_percent
    )

    return result
