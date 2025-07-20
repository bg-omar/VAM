import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.special import genlaguerre

# Constants (from VAM and QM equivalence)
a0 = 5.29177210903e-11  # Bohr radius in meters
n_values = [1, 2, 3, 4]  # Principal quantum numbers
r = np.linspace(0, 10 * a0, 500)  # Radial range

# Define quantum radial wavefunction amplitude (Schrödinger)
def quantum_radial_wavefunction(r, n):
    """Computes the quantum radial wavefunction R_{n0}(r) for s-orbitals."""
    prefactor = np.sqrt((2 / (n * a0))**3 * math.factorial(n - 1) / (2 * n * math.factorial(n)))
    rho = 2 * r / (n * a0)  # Scaled radius
    laguerre_poly = genlaguerre(n - 1, 2)(rho)  # Associated Laguerre polynomial
    return prefactor * np.exp(-rho / 2) * laguerre_poly

# Define VAM vorticity-based wavefunction amplitude
def vam_vorticity_wavefunction(r, n):
    """Computes the vorticity-based wavefunction amplitude in VAM."""
    prefactor = np.sqrt((2 / (n * a0))**3)  # Adjusted prefactor
    rho = 2 * r / (n * a0)  # Scaled radius
    laguerre_poly = genlaguerre(n - 1, 2)(rho)  # Vortex circulation equivalent
    return prefactor * np.exp(-rho / 2) * np.sin(rho * np.pi / (2 * n)) * laguerre_poly

# Compute wavefunctions
qm_wavefunctions = {n: quantum_radial_wavefunction(r, n) for n in n_values}
vam_wavefunctions = {n: vam_vorticity_wavefunction(r, n) for n in n_values}

# Create figure for comparison
fig, axes = plt.subplots(2, 1, figsize=(8, 10))

# Plot each n-level for QM and VAM models
for n in n_values:
    axes[0].plot(r / a0, qm_wavefunctions[n], label=f"n={n} (QM)")
    axes[1].plot(r / a0, vam_wavefunctions[n], label=f"n={n} (VAM)")

# Quantum Model Plot
axes[0].set_xlabel(r"$r / a_0$ (Bohr radii)")
axes[0].set_ylabel(r"$\psi_{n0}(r)$ (Quantum Wavefunction)")
axes[0].set_title("Quantum Radial Schrödinger Wavefunctions")
axes[0].legend()
axes[0].grid()

# VAM Model Plot
axes[1].set_xlabel(r"$r / a_0$ (Bohr radii)")
axes[1].set_ylabel(r"$\omega_{n0}(r)$ (Vorticity Wavefunction)")
axes[1].set_title("VAM Radial Vorticity Equivalent of Schrödinger Wavefunctions")
axes[1].legend()
axes[1].grid()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

plt.show()