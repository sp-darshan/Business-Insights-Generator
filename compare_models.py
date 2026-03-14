from app.data_preprocessor import load_and_clean_data, get_monthly_revenue
from app.arima_model import forecast_revenue
from app.baseline_model import naive_forecast


df = load_and_clean_data("data/online_retail.csv")
monthly_revenue = get_monthly_revenue(df)

# ARIMA
arima_result = forecast_revenue(monthly_revenue)
arima_eval = arima_result["evaluation"]

# Baseline
baseline_eval = naive_forecast(monthly_revenue)

print("\nModel Comparison\n")

print("Baseline Model:")
print(baseline_eval)

print("\nARIMA Model:")
print(arima_eval)

import matplotlib.pyplot as plt

models = ["Naive", "ARIMA"]
rmse = [baseline_eval["rmse"], arima_eval["rmse"]]

plt.bar(models, rmse)

plt.title("Model Comparison (RMSE)")
plt.ylabel("Error")

plt.show()