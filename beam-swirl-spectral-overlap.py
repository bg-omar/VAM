import numpy as np
import matplotlib.pyplot as plt

# Constants
C_e = 1093845.63  # Vortex angular velocity in m/s
r_c = 1.40897e-15  # Vortex core radius in meters

# Beam parameters
omega_0 = C_e / r_c  # Central angular frequency of the beam
delta_omega = 0.1 * omega_0  # Beam spectral width

# Frequency range
omega = np.linspace(0.8 * omega_0, 1.2 * omega_0, 1000)

# Beam spectral density (Gaussian)
rho_beam = np.exp(-((omega - omega_0)**2) / (2 * delta_omega**2))

# Knot resonance parameters for 3 knot species (e.g., trefoil, figure-8, double-ring)
omega_n = [omega_0, 1.05 * omega_0, 0.95 * omega_0]
Gamma_n = [0.05 * omega_0] * 3
B_n = [1.0, 0.8, 0.6]  # Arbitrary coupling strengths

# Knot absorption spectrum
sigma_knot = np.zeros_like(omega)
for B, w_n, G in zip(B_n, omega_n, Gamma_n):
    sigma_knot += B * (G**2) / ((omega - w_n)**2 + G**2)

# Fusion yield integrand
fusion_yield_density = rho_beam * sigma_knot

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(omega / 1e20, rho_beam, label='Beam Spectrum $\\rho_{\\mathrm{beam}}(\\omega)$', linestyle='--')
plt.plot(omega / 1e20, sigma_knot, label='Knot Absorption $\\sigma_{\\mathrm{knot}}(\\omega)$', linestyle='-.')
plt.plot(omega / 1e20, fusion_yield_density, label='Fusion Yield Density $Y_{\\mathrm{VAM}}(\\omega)$', linewidth=2)
plt.xlabel("Angular Frequency $\\omega$ (×10²⁰ rad/s)")
plt.ylabel("Normalized Intensity")
plt.title("VAM Beam–Swirl Spectral Overlap")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()