import matplotlib.pyplot as plt
from app.data_preprocessor import load_and_clean_data, get_monthly_revenue
from app.arima_model import forecast_revenue


df = load_and_clean_data("data/online_retail.csv")
monthly_revenue = get_monthly_revenue(df)

result = forecast_revenue(monthly_revenue)

# recreate split
split_index = int(len(monthly_revenue) * 0.8)

train = monthly_revenue[:split_index]
test = monthly_revenue[split_index:]

pred = result["test_prediction"]

plt.figure(figsize=(8,5))

plt.plot(test.values, label="Actual", marker='o')
plt.plot(pred, label="Predicted", marker='o')

plt.title("ARIMA Forecast Validation")
plt.xlabel("Test Months")
plt.ylabel("Revenue")
plt.legend()
plt.grid(True)

plt.show()