import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


def naive_forecast(monthly_series):

    split_index = int(len(monthly_series) * 0.8)

    train = monthly_series[:split_index]
    test = monthly_series[split_index:]

    # Naive prediction = last value of train repeated
    last_value = train.iloc[-1]

    predictions = [last_value] * len(test)

    rmse = np.sqrt(mean_squared_error(test, predictions))
    mae = mean_absolute_error(test, predictions)

    mape = np.mean(
        np.abs((test - predictions) / np.where(test == 0, 1, test))
    ) * 100

    return {
        "rmse": float(rmse),
        "mae": float(mae),
        "mape": float(mape)
    }