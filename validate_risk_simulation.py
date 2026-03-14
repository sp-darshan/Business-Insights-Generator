import numpy as np
import matplotlib.pyplot as plt

from app.data_preprocessor import load_and_clean_data, get_monthly_revenue
from app.arima_model import forecast_revenue
from app.monte_carlo import monte_carlo_simulation


df = load_and_clean_data("data/online_retail.csv")
monthly_revenue = get_monthly_revenue(df)

forecast = forecast_revenue(monthly_revenue)

result = monte_carlo_simulation(monthly_revenue, forecast)

print("\nMonte Carlo Risk Analysis\n")

print("Probability of Decline:", result["probability_of_decline"])
print("Worst Case Revenue:", result["worst_case_revenue"])
print("Best Case Revenue:", result["best_case_revenue"])
print("Volatility Index:", result["volatility_index_percent"])

simulations = []

historical_returns = monthly_revenue.pct_change().dropna()

mean_return = historical_returns.mean()
volatility = historical_returns.std()

last_revenue = monthly_revenue.iloc[-1]

steps = 3
runs = 1000

for _ in range(runs):

    revenue = last_revenue

    for _ in range(steps):

        shock = np.random.normal(mean_return, volatility)
        shock = np.clip(shock, -0.4, 0.4)

        revenue = revenue * (1 + shock)

    simulations.append(revenue)

simulations = np.array(simulations)

plt.figure(figsize=(8,5))

plt.hist(simulations, bins=30, alpha=0.7)

plt.axvline(np.percentile(simulations,5), color='red', label="Worst Case")
plt.axvline(np.percentile(simulations,95), color='green', label="Best Case")

plt.title("Monte Carlo Revenue Risk Distribution")
plt.xlabel("Simulated Revenue")
plt.ylabel("Frequency")

plt.legend()
plt.show()