import numpy as np
import matplotlib.pyplot as plt

from app.data_preprocessor import load_and_clean_data, get_monthly_revenue
from app.vae import generate_scenarios
from app.gan_model import generate_synthetic_data


df = load_and_clean_data("data/online_retail.csv")
monthly_revenue = get_monthly_revenue(df)

# Real data
real_values = monthly_revenue.values

# VAE
vae_output = generate_scenarios(monthly_revenue)
vae_values = np.array(vae_output["simulated_revenue_scenarios"])

# GAN
gan_output = generate_synthetic_data(monthly_revenue)
gan_values = np.array(gan_output["synthetic_revenue_samples"])


print("\nREAL DATA")
print("Mean:", np.mean(real_values))
print("Std:", np.std(real_values))

print("\nVAE GENERATED")
print("Mean:", np.mean(vae_values))
print("Std:", np.std(vae_values))

print("\nGAN GENERATED")
print("Mean:", np.mean(gan_values))
print("Std:", np.std(gan_values))

plt.figure(figsize=(8,5))

plt.hist(real_values, bins=6, alpha=0.6, label="Real Data")
plt.hist(vae_values, bins=6, alpha=0.6, label="VAE Generated")
plt.hist(gan_values, bins=6, alpha=0.6, label="GAN Generated")

plt.title("Distribution Comparison: Real vs Generated Revenue")
plt.xlabel("Revenue")
plt.ylabel("Frequency")

plt.legend()
plt.show()
