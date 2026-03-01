from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


def forecast_revenue(monthly_series, steps=3):

    if len(monthly_series) < 6:
        raise ValueError("Not enough data for forecasting.")

    # -------------------------
    # 1️⃣ Train-Test Split
    # -------------------------
    train_size = int(len(monthly_series) * 0.8)
    train = monthly_series[:train_size]
    test = monthly_series[train_size:]

    # -------------------------
    # 2️⃣ Use Stable ARIMA(1,1,1)
    # -------------------------
    model = SARIMAX(
        train,
        order=(0, 1, 1),
        trend='c',  # include drift
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    model_fit = model.fit(disp=False)

    # -------------------------
    # 3️⃣ Evaluate
    # -------------------------
    test_forecast = model_fit.forecast(steps=len(test))

    rmse = np.sqrt(mean_squared_error(test, test_forecast))
    mae = mean_absolute_error(test, test_forecast)

    mape = np.mean(
        np.abs((test - test_forecast) / np.where(test == 0, 1, test))
    ) * 100

    # -------------------------
    # 4️⃣ Retrain on FULL Data
    # -------------------------
    final_model = SARIMAX(
        monthly_series,
        order=(0,1,1),
        trend='c',
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    final_fit = final_model.fit(disp=False)

    future_forecast = final_fit.forecast(steps=steps)
    # print("Historical min:", monthly_series.min())
    # print("Historical max:", monthly_series.max())

    # # -------------------------
    # # DEBUG: Plot Actual vs Forecast
    # # -------------------------
    # import matplotlib.pyplot as plt

    # plt.figure(figsize=(8, 4))

    # # Plot actual historical data
    # monthly_series.plot(label="Actual")
    # plt.legend()
    # plt.title("Actual")
    # plt.show()

    # # Create index for forecast continuation
    # forecast_index = range(len(monthly_series), len(monthly_series) + steps)

    # plt.plot(forecast_index, future_forecast, label="Forecast", marker='o')

    # plt.legend()
    # plt.title("Forecast")
    # plt.show()

    # # Plot actual historical data
    # monthly_series.plot(label="Actual")

    # # Create index for forecast continuation
    # forecast_index = range(len(monthly_series), len(monthly_series) + steps)

    # plt.plot(forecast_index, future_forecast, label="Forecast", marker='o')

    # plt.legend()
    # plt.title("Actual vs Forecast")
    # plt.show()
    

    last_value = monthly_series.iloc[-1]
    trend = "increasing" if future_forecast.iloc[-1] > last_value else "decreasing"

    return {
        "next_months_forecast": [float(x) for x in future_forecast],
        "trend": trend,
        "evaluation": {
            "rmse": float(rmse),
            "mae": float(mae),
            "mape": float(mape)
        },
        "model_details": {
            "order": (0, 1, 1)
        }
    }