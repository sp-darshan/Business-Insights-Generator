"""
Script to train GAN and visualize Generator vs Discriminator Loss
"""
import sys
sys.path.insert(0, 'd:\\Projects\\College\\business_insights_generator')

from app.data_preprocessor import load_and_clean_data, get_monthly_revenue
from app.gan_model import generate_synthetic_data
import matplotlib.pyplot as plt

# Load data
print("Loading data...")
df = load_and_clean_data("data/online_retail.csv")
monthly_revenue = get_monthly_revenue(df)

print(f"Data loaded. Monthly revenue shape: {monthly_revenue.shape}")
print(f"Revenue range: ${monthly_revenue.min():.2f} - ${monthly_revenue.max():.2f}")

# Train GAN and generate synthetic data
print("\nTraining GAN model (this may take a few moments)...")
result = generate_synthetic_data(monthly_revenue, num_samples=6)

print("\nGAN Training Complete!")
print(f"Generated {len(result['synthetic_revenue_samples'])} synthetic samples")
print(f"Synthetic samples: {result['synthetic_revenue_samples']}")

# Extract and plot training history
if 'training_history' in result:
    history = result['training_history']
    
    # Create a high-quality loss plot
    plt.figure(figsize=(12, 7))
    
    epochs = range(1, len(history['generator_losses']) + 1)
    
    plt.plot(epochs, history['generator_losses'], 'b-', label='Generator Loss', 
             linewidth=2, alpha=0.8)
    plt.plot(epochs, history['discriminator_losses'], 'r-', label='Discriminator Loss', 
             linewidth=2, alpha=0.8)
    
    plt.xlabel('Epoch', fontsize=12, fontweight='bold')
    plt.ylabel('Loss', fontsize=12, fontweight='bold')
    plt.title('GAN Training: Generator vs Discriminator Loss', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11, loc='upper right')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('gan_loss_plot.png', dpi=300, bbox_inches='tight')
    print("\n✓ Loss plot saved as 'gan_loss_plot.png'")
    
    plt.show()
    
    # Print final loss values
    print(f"\nFinal Generator Loss: {history['generator_losses'][-1]:.4f}")
    print(f"Final Discriminator Loss: {history['discriminator_losses'][-1]:.4f}")
    
    # Print statistics
    import numpy as np
    print(f"\nGenerator Loss Statistics:")
    print(f"  Min: {np.min(history['generator_losses']):.4f}")
    print(f"  Max: {np.max(history['generator_losses']):.4f}")
    print(f"  Mean: {np.mean(history['generator_losses']):.4f}")
    
    print(f"\nDiscriminator Loss Statistics:")
    print(f"  Min: {np.min(history['discriminator_losses']):.4f}")
    print(f"  Max: {np.max(history['discriminator_losses']):.4f}")
    print(f"  Mean: {np.mean(history['discriminator_losses']):.4f}")
