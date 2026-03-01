import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler


# -----------------------
# Generator
# -----------------------
class Generator(nn.Module):
    def __init__(self, noise_dim=5):
        super(Generator, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(noise_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Tanh()   # keeps output bounded
        )

    def forward(self, z):
        return self.model(z)


# -----------------------
# Discriminator
# -----------------------
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(1, 32),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.2),
            nn.Linear(32, 16),
            nn.LeakyReLU(0.2),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)


# -----------------------
# GAN Training Function
# -----------------------
def generate_synthetic_data(monthly_series, num_samples=6):

    values = monthly_series.values.reshape(-1, 1)

    scaler = MinMaxScaler(feature_range=(-1, 1))
    values_scaled = scaler.fit_transform(values)

    real_data = torch.FloatTensor(values_scaled)

    noise_dim = 5
    generator = Generator(noise_dim)
    discriminator = Discriminator()

    criterion = nn.BCELoss()

    g_optimizer = torch.optim.Adam(generator.parameters(), lr=0.001)
    d_optimizer = torch.optim.Adam(discriminator.parameters(), lr=0.001)

    epochs = 800
    batch_size = min(8, len(real_data))

    for epoch in range(epochs):

        # Mini-batch sampling
        idx = np.random.randint(0, len(real_data), batch_size)
        real_batch = real_data[idx]

        # -------------------
        # Train Discriminator
        # -------------------
        d_optimizer.zero_grad()

        # Label smoothing
        real_labels = torch.ones(batch_size, 1) * 0.9
        fake_labels = torch.zeros(batch_size, 1)

        outputs_real = discriminator(real_batch)
        d_loss_real = criterion(outputs_real, real_labels)

        noise = torch.randn(batch_size, noise_dim)
        fake_data = generator(noise)
        outputs_fake = discriminator(fake_data.detach())
        d_loss_fake = criterion(outputs_fake, fake_labels)

        d_loss = d_loss_real + d_loss_fake
        d_loss.backward()
        d_optimizer.step()

        # -------------------
        # Train Generator
        # -------------------
        g_optimizer.zero_grad()

        noise = torch.randn(batch_size, noise_dim)
        fake_data = generator(noise)
        outputs = discriminator(fake_data)

        g_loss = criterion(outputs, real_labels)
        g_loss.backward()
        g_optimizer.step()

    # -------------------
    # Generate Samples
    # -------------------
    with torch.no_grad():
        noise = torch.randn(num_samples * 5, noise_dim)
        synthetic = generator(noise).numpy()

    synthetic = scaler.inverse_transform(synthetic)

    # Add mild diversification noise
    std_dev = monthly_series.std() * 0.03
    synthetic += np.random.normal(0, std_dev, synthetic.shape)

    # Keep realistic bounds
    min_val = monthly_series.min()
    max_val = monthly_series.max()

    synthetic = np.clip(synthetic, min_val, max_val)

    # Remove duplicates
    synthetic = np.unique(synthetic)

    if len(synthetic) < num_samples:
        # If collapse still happens, resample with noise
        extra = np.random.normal(
            monthly_series.mean(),
            monthly_series.std() * 0.5,
            num_samples
        )
        synthetic = np.concatenate([synthetic.flatten(), extra])

    synthetic = synthetic[:num_samples]

    return {
        "synthetic_revenue_samples": [float(x) for x in synthetic]
    }