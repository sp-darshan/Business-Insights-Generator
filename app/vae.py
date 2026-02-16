import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class VAE(nn.Module):
    def __init__(self, input_dim, latent_dim=2):
        super(VAE, self).__init__()

        self.fc1 = nn.Linear(input_dim, 16)
        self.fc21 = nn.Linear(16, latent_dim)  # mean
        self.fc22 = nn.Linear(16, latent_dim)  # log variance
        self.fc3 = nn.Linear(latent_dim, 16)
        self.fc4 = nn.Linear(16, input_dim)

    def encode(self, x):
        h = torch.relu(self.fc1(x))
        return self.fc21(h), self.fc22(h)

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        h = torch.relu(self.fc3(z))
        return self.fc4(h)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar

def generate_scenarios(monthly_series, num_samples=6):

    values = monthly_series.values.reshape(-1, 1)

    scaler = MinMaxScaler()
    values_scaled = scaler.fit_transform(values)

    data_tensor = torch.FloatTensor(values_scaled)

    input_dim = 1
    model = VAE(input_dim)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    def loss_function(recon_x, x, mu, logvar):
        mse = nn.functional.mse_loss(recon_x, x)
        kld = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
        return mse + kld

    # Train
    epochs = 100
    for epoch in range(epochs):
        optimizer.zero_grad()
        recon_batch, mu, logvar = model(data_tensor)
        loss = loss_function(recon_batch, data_tensor, mu, logvar)
        loss.backward()
        optimizer.step()

    # Generate new samples
    with torch.no_grad():
        z = torch.randn(num_samples, 2)
        generated = model.decode(z).numpy()

    generated = scaler.inverse_transform(generated)

    return {
        "simulated_revenue_scenarios": [float(x[0]) for x in generated]
    }
