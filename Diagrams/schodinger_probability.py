import numpy as np
import matplotlib.pyplot as plt
from scipy.special import genlaguerre
from scipy.constants import physical_constants

# Constants
a0 = physical_constants["Bohr radius"][0]  # Bohr radius in meters
n = 3  # Principal quantum number (modify as needed)

# Define radial wavefunction R_n0(r)
def radial_wavefunction(n, r):
    """Computes the radial wavefunction for the nth s-orbital (ℓ=0)."""
    prefactor = np.sqrt((2 / (n * a0))**3 * np.emath.factorial(n - 1) / (2 * n * np.emath.factorial(n)))
    rho = 2 * r / (n * a0)  # Scaled radius
    laguerre_poly = genlaguerre(n - 1, 2)(rho)  # Associated Laguerre polynomial
    return prefactor * np.exp(-rho / 2) * laguerre_poly

# Generate radial points
r = np.linspace(0, 20 * a0, 1000)  # Range of r values

# Compute wavefunction and probability density
psi_r = radial_wavefunction(n, r)
probability_density = psi_r**2

# Plot the radial probability density
plt.figure(figsize=(8, 5))
plt.plot(r / a0, probability_density, label=f"$n = {n}$ s-orbital")
plt.xlabel(r"$r / a_0$ (Bohr radii)")
plt.ylabel(r"$|\psi_{n0}(r)|^2$")
plt.title(f"Radial Probability Density for Hydrogen-like Atom (n={n})")
plt.legend()
plt.grid()
plt.show()
