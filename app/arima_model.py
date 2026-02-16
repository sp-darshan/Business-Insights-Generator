from statsmodels.tsa.arima.model import ARIMA


def forecast_revenue(monthly_series, steps=3):

    model = ARIMA(monthly_series, order=(2, 1, 2))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=steps)

    last_value = monthly_series.iloc[-1]
    forecast_mean = forecast.mean()

    trend = "increasing" if forecast_mean > last_value else "decreasing"

    return {
        "next_months_forecast": [float(x) for x in forecast],
        "trend": trend
    }
