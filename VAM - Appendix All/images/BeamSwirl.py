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
plt.savefig("vam_swirl_yield_plot.png")
plt.show()






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
plt.savefig('vam_time_response_plot.png')





# Create zoomed-in plot for the central part of the response
zoom_range = (t > -5e-15) & (t < 5e-15)

plt.figure(figsize=(10, 4))
for tau, F_t, S_t in responses:
    plt.plot(t[zoom_range] * 1e16, S_t[zoom_range], label=f'τ = {tau*1e15:.1f} fs')
plt.title('Zoomed-In Vortex Response $S(t)$ (|t| < 5 fs)')
plt.xlabel('Time (fs)')
plt.ylabel('Response Amplitude (a.u.)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('vam_time_response_zoom_plot.png')
plt.show()
