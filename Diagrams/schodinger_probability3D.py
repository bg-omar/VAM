import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import genlaguerre
from scipy.constants import physical_constants

# Constants
a0 = physical_constants["Bohr radius"][0]  # Bohr radius in meters
n_values = [1, 2, 3, 4]  # Principal quantum numbers to visualize

# Define radial wavefunction R_n0(r)
def radial_wavefunction(n, r):
    """Computes the radial wavefunction for the nth s-orbital (ℓ=0)."""
    prefactor = np.sqrt((2 / (n * a0))**3 * np.math.factorial(n - 1) / (2 * n * np.math.factorial(n)))
    rho = 2 * r / (n * a0)  # Scaled radius
    laguerre_poly = genlaguerre(n - 1, 2)(rho)  # Associated Laguerre polynomial
    return prefactor * np.exp(-rho / 2) * laguerre_poly

# Set up 3D plot
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Generate spherical coordinates
theta = np.linspace(0, np.pi, 100)  # Azimuthal angle
phi = np.linspace(0, 2 * np.pi, 100)  # Polar angle
theta, phi = np.meshgrid(theta, phi)

# Loop over different orbitals
colors = ['b', 'r', 'g', 'm']
for idx, n in enumerate(n_values):
    r = np.linspace(0, 10 * a0, 100)  # Radial distance
    psi_r = radial_wavefunction(n, r)  # Compute radial wavefunction
    probability_density = np.abs(psi_r) ** 2  # Compute probability density

    # Normalize for visualization
    r_scaled = probability_density / np.max(probability_density) * (n / 2)  # Normalize and scale

    # Convert spherical to Cartesian coordinates
    X = r_scaled[:, None, None] * np.sin(theta) * np.cos(phi)
    Y = r_scaled[:, None, None] * np.sin(theta) * np.sin(phi)
    Z = r_scaled[:, None, None] * np.cos(theta)

    # Plot the isosurface for each orbital
    ax.plot_surface(X[:, :, 50], Y[:, :, 50], Z[:, :, 50], color=colors[idx], alpha=0.6, edgecolor='k', linewidth=0.2)

# Labels and visualization adjustments
ax.set_xlabel("X (Bohr radii)")
ax.set_ylabel("Y (Bohr radii)")
ax.set_zlabel("Z (Bohr radii)")
ax.set_title("3D Visualization of Hydrogen-like s-Orbitals")
ax.view_init(elev=30, azim=45)  # Adjust the viewing angle

plt.show()