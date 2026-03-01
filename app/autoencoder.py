import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class AutoEncoder(nn.Module):
    def __init__(self, input_dim):
        super(AutoEncoder, self).__init__()

        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 8),
            nn.ReLU(),
            nn.Linear(8, 4)
        )

        self.decoder = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, input_dim)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


def detect_anomalies(daily_series):

    # Convert to numpy
    values = daily_series.values.reshape(-1, 1)

    # Normalize
    scaler = MinMaxScaler()
    values_scaled = scaler.fit_transform(values)

    # Convert to tensor
    data_tensor = torch.FloatTensor(values_scaled)

    input_dim = 1
    model = AutoEncoder(input_dim)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    # Train
    epochs = 50
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(data_tensor)
        loss = criterion(outputs, data_tensor)
        loss.backward()
        optimizer.step()

    # Reconstruction
    with torch.no_grad():
        reconstructed = model(data_tensor)
        reconstruction_error = torch.mean(
            (data_tensor - reconstructed) ** 2,
            dim=1
        ).numpy()

    # Threshold (mean + 2 std)
    threshold = reconstruction_error.mean() + 2 * reconstruction_error.std()

    anomaly_indices = np.where(reconstruction_error > threshold)[0]

    anomaly_dates = daily_series.index[anomaly_indices].strftime("%Y-%m-%d").tolist()

    return {
        "anomaly_days": anomaly_dates,
        "anomaly_count": len(anomaly_dates),
        "risk_level": "high" if len(anomaly_dates) > 5 else "medium" if len(anomaly_dates) > 0 else "low",
        "threshold": float(threshold)
    }
