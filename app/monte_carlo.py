import numpy as np


def monte_carlo_simulation(monthly_series, forecast_output, simulations=500):

    historical_returns = monthly_series.pct_change().dropna()

    mean_return = historical_returns.mean()
    volatility = historical_returns.std()

    last_revenue = monthly_series.iloc[-1]

    simulated_end_values = []

    steps = len(forecast_output["next_months_forecast"])

    for _ in range(simulations):

        revenue = last_revenue

        for _ in range(steps):

            shock = np.random.normal(mean_return, volatility)

            # Cap unrealistic monthly shocks
            shock = np.clip(shock, -0.4, 0.4)

            revenue = revenue * (1 + shock)

        simulated_end_values.append(revenue)

    simulated_end_values = np.array(simulated_end_values)

    probability_decline = np.mean(simulated_end_values < last_revenue)

    worst_case = np.percentile(simulated_end_values, 5)
    best_case = np.percentile(simulated_end_values, 95)

    volatility_index = volatility * 100

    return {
        "probability_of_decline": float(probability_decline),
        "worst_case_revenue": float(worst_case),
        "best_case_revenue": float(best_case),
        "volatility_index_percent": float(volatility_index)
    }