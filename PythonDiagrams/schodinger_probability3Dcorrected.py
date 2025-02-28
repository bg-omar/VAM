import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import genlaguerre
from scipy.constants import physical_constants
import matplotlib.colors as mcolors

# Constants
a0 = physical_constants["Bohr radius"][0]  # Bohr radius in meters
n_values = [1, 2, 3, 4]  # Principal quantum numbers to visualize
num_points = 5000  # Number of random points for cloud visualization

# Define Schrödinger wavefunction (correct formula)
def schrodinger_wavefunction(r, n):
    """Computes the correct radial Schrödinger wavefunction for s-orbitals (ℓ=0)."""
    prefactor = np.sqrt((2 / (n * a0))**3 * np.math.factorial(n - 1) / (2 * n * np.math.factorial(n)))
    rho = 2 * r / (n * a0)  # Scaled radius
    laguerre_poly = genlaguerre(n - 1, 2)(rho)  # Associated Laguerre polynomial
    return prefactor * np.exp(-rho / 2) * laguerre_poly

# Set up 3D plot
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Loop through different orbitals
for idx, n in enumerate(n_values):
    # Generate random points in spherical coordinates
    r = np.random.rand(num_points) * (n + 1) * a0  # Scale range per quantum number
    theta = np.random.rand(num_points) * np.pi
    phi = np.random.rand(num_points) * 2 * np.pi

    # Compute wavefunction and probability density
    psi_r = schrodinger_wavefunction(r, n)
    prob_density = np.abs(psi_r) ** 2  # Compute probability density

    # Normalize probability density for visualization
    prob_density /= np.max(prob_density)  # Normalize to range [0, 1]

    # Convert spherical to Cartesian coordinates
    X = r * np.sin(theta) * np.cos(phi)
    Y = r * np.sin(theta) * np.sin(phi)
    Z = r * np.cos(theta)

    # Convert probability to color intensity
    colors = plt.get_cmap('viridis')(prob_density)  # Use a colormap (e.g., 'viridis')

    # Scatter plot using colored points
    ax.scatter(X, Y, Z, color=colors, alpha=0.5, s=2)

# Labels and visualization adjustments
ax.set_xlabel("X (Bohr radii)")
ax.set_ylabel("Y (Bohr radii)")
ax.set_zlabel("Z (Bohr radii)")
ax.set_title("3D Schrödinger Wavefunction for Hydrogen s-Orbitals")
ax.view_init(elev=30, azim=45)  # Adjust the viewing angle

plt.show()
