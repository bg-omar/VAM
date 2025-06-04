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
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()


import numpy as np
import matplotlib.pyplot as plt

# Constants (from VAM)
Ce = 1.09384563e6       # m/s (vortex core tangential velocity)
rc = 1.40897017e-15     # m (vortex core radius)
omega_0 = Ce / rc       # beam central angular frequency
delta_omega = 0.1 * omega_0  # beam spectral width (10% spread)

# Beam spectral density: Gaussian centered at omega_0
def rho_beam(omega):
    A = 1.0  # normalized
    return A * np.exp(-(omega - omega_0)**2 / (2 * delta_omega**2))

# Vortex knot absorption spectrum: sum of Lorentzians
def sigma_knot(omega, omega_n_list, Gamma_n_list, B_n_list):
    result = np.zeros_like(omega)
    for omega_n, Gamma_n, B_n in zip(omega_n_list, Gamma_n_list, B_n_list):
        result += B_n * Gamma_n**2 / ((omega - omega_n)**2 + Gamma_n**2)
    return result

# Define vortex species
omega_n_list = np.array([
    omega_0 * 0.95,  # Slightly below center
    omega_0 * 1.00,  # Resonant
    omega_0 * 1.05   # Slightly above center
])
Gamma_n_list = np.array([
    0.02 * omega_0,
    0.01 * omega_0,
    0.02 * omega_0
])
B_n_list = np.array([1.0, 2.0, 1.0])

# Frequency axis for plotting
omega = np.linspace(0.9 * omega_0, 1.1 * omega_0, 1000)
beam = rho_beam(omega)
knot = sigma_knot(omega, omega_n_list, Gamma_n_list, B_n_list)
yield_curve = beam * knot

# Plot
plt.figure(figsize=(10, 6))
plt.plot(omega, beam, label=r'$\rho_{\mathrm{beam}}(\omega)$', linestyle='--')
plt.plot(omega, knot, label=r'$\sigma_{\mathrm{knot}}(\omega)$', linestyle=':')
plt.plot(omega, yield_curve, label=r'$Y_{\mathrm{VAM}}(\omega)$', linewidth=2)
plt.xlabel('Angular Frequency $\omega$ (rad/s)')
plt.ylabel('Amplitude (a.u.)')
plt.title('Swirl Resonance Fusion Yield in VAM')
plt.legend()
plt.grid(True)
plt.tight_layout()

script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()


import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftfreq

# Time domain setup
N = 2048
T = 1e-18  # time step (s)
t = np.linspace(-N//2 * T, N//2 * T, N)
dt = T
freqs = fftfreq(N, dt) * 2 * np.pi  # angular frequencies
omega = np.fft.fftshift(freqs)

# Define spectral absorption function: Lorentzian sum (same as before)
def sigma_knot_omega(omega):
    return sigma_knot(omega, omega_n_list, Gamma_n_list, B_n_list)

# Gaussian-modulated pulse
def pulse(t, omega0, tau):
    return np.exp(-t**2 / tau**2) * np.cos(omega0 * t)

# Inverse Fourier transform of sigma_knot to get K(t)
sigma_vals = sigma_knot_omega(np.fft.fftshift(omega))
K_freq = np.fft.ifft(np.fft.ifftshift(sigma_vals))
K_t = np.fft.fftshift(np.real(K_freq))  # response function

# Pulse durations to test (short and long)
taus = [1e-18, 5e-18, 1e-17]
responses = []

for tau in taus:
    F_t = pulse(t, omega_0, tau)
    S_t = np.convolve(F_t, K_t, mode='same') * dt
    responses.append((tau, F_t, S_t))

# Plot results
plt.figure(figsize=(12, 8))
for tau, F_t, S_t in responses:
    plt.plot(t * 1e15, S_t, label=f'Pulse τ = {tau*1e15:.1f} fs')
plt.title('Time-Domain Vortex Response $S(t)$ for Varying Pulse Widths')
plt.xlabel('Time (fs)')
plt.ylabel('Response Amplitude (a.u.)')
plt.grid(True)
plt.legend()
plt.tight_layout()
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}3.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()

# Create zoomed-in plot for the central part of the response
zoom_range = (t > -5e-15) & (t < 5e-15)

plt.figure(figsize=(10, 4))
for tau, F_t, S_t in responses:
    plt.plot(t[zoom_range] * 1e15, S_t[zoom_range], label=f'τ = {tau*1e15:.1f} fs')
plt.title('Zoomed-In Vortex Response $S(t)$ (|t| < 5 fs)')
plt.xlabel('Time (fs)')
plt.ylabel('Response Amplitude (a.u.)')
plt.grid(True)
plt.legend()
plt.tight_layout()
filename = f"{script_name}4.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()


import numpy as np
import matplotlib.pyplot as plt

# Constants
hbar = 1.055e-34  # Planck's reduced constant [J·s]
eV_to_J = 1.602e-13  # conversion factor [MeV to J]
E_gamma = 5.0  # MeV

# Calculate omega_res for gamma-ray
omega_res = (E_gamma * eV_to_J) / hbar

# VAM-based omega_0
C_e = 1.09384563e6  # m/s
r_c = 1.40897017e-15  # m
omega_0 = C_e / r_c

# Plot both frequencies
labels = ['Gamma-resonance (B-11)', 'VAM core ω₀']
frequencies = [omega_res, omega_0]

plt.bar(labels, frequencies, color=['steelblue', 'darkorange'])
plt.ylabel("Resonant Frequency [rad/s]")
plt.title("Swirl Resonance Alignment in LENR (Boron-11)")
plt.grid(True, axis='y')

plt.tight_layout()
filename = f"{script_name}5.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()

import numpy as np
import matplotlib.pyplot as plt

# VAM constants
omega_n = 7.763e20  # rad/s
delta_omega = 0.05 * omega_n

# Gaussian beam profile
def rho_beam(omega, omega_0):
    return np.exp(-((omega - omega_0) ** 2) / (2 * delta_omega ** 2))

# Lorentzian knot absorption
def sigma_knot(omega, omega_n, Gamma):
    return Gamma**2 / ((omega - omega_n)**2 + Gamma**2)

# Sweep detuning
deltas = np.linspace(-0.3, 0.3, 100) * omega_n
Gamma = 0.1 * omega_n
omega = np.linspace(omega_n - 4 * Gamma, omega_n + 4 * Gamma, 1000)

yields = []
for delta in deltas:
    omega_0 = omega_n + delta
    integrand = rho_beam(omega, omega_0) * sigma_knot(omega, omega_n, Gamma)
    Y = np.trapz(integrand, omega)
    yields.append(Y)

# Plot detuning response
plt.figure(figsize=(8, 5))
plt.plot(deltas / omega_n, yields)
plt.xlabel("Normalized Detuning $(\\omega_0 - \\omega_n)/\\omega_n$")
plt.ylabel("Fusion Yield $Y_{\\mathrm{VAM}}$")
plt.title("Fusion Yield vs Detuning")
plt.grid(True)
plt.tight_layout()
filename = f"{script_name}6.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()


# Sweep over Gamma values and compute yield
Gamma_factors = [0.01, 0.03, 0.1, 0.3]
yields_gamma = []

omega_0 = omega_n  # Fixed at resonance
for factor in Gamma_factors:
    Gamma = factor * omega_n
    integrand = rho_beam(omega, omega_0) * sigma_knot(omega, omega_n, Gamma)
    Y = np.trapz(integrand, omega)
    yields_gamma.append(Y)

# Plot yield vs Gamma
plt.figure(figsize=(8, 5))
plt.plot(Gamma_factors, yields_gamma, marker='o')
plt.xlabel("Damping Width $\\Gamma / \\omega_0$")
plt.ylabel("Fusion Yield $Y_{\\mathrm{VAM}}$")
plt.title("Fusion Yield vs Resonance Width")
plt.grid(True)
plt.tight_layout()
filename = f"{script_name}7.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution


plt.show()
