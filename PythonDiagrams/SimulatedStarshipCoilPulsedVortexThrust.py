# Re-run full script after kernel reset
import numpy as np
import matplotlib.pyplot as plt

# Constants
rho_ae = 7.0e-7  # kg/m^3, Æther density
C_e = 1.09384563e6  # m/s, vortex core tangential velocity
r = 0.02  # m, coil effective radius
A = np.pi * r**2  # m^2, coil cross-sectional area
delta_z = 0.01  # m, effective coil height
V0 = 2000  # peak voltage in volts
f = 500  # Hz, drive frequency
omega = 2 * np.pi * f  # angular frequency
alpha_E = (2 * np.pi * r * C_e) / V0  # vortex-voltage coupling factor

# Coupling constant kappa
kappa = (rho_ae * A * delta_z * alpha_E) / (2 * np.pi)

# Time domain
t = np.linspace(0, 0.02, 5000)  # simulate 20 ms at high resolution

# 3-phase sinusoidal voltage waveforms
V_A = V0 * np.sin(omega * t)
V_B = V0 * np.sin(omega * t + 2 * np.pi / 3)
V_C = V0 * np.sin(omega * t + 4 * np.pi / 3)

# Time derivatives (dV/dt)
dV_A_dt = np.gradient(V_A, t)
dV_B_dt = np.gradient(V_B, t)
dV_C_dt = np.gradient(V_C, t)

# Total instantaneous thrust from all 3 phases
T_total = kappa * (dV_A_dt + dV_B_dt + dV_C_dt)  # Net force in N
T_total_g = T_total * 101.97  # Convert N to grams-force

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(t * 1000, T_total_g, color='purple', label='Net VAM Thrust (g)')
plt.xlabel("Time (ms)")
plt.ylabel("Thrust (grams)")
plt.title("Simulated Starship Coil Pulsed Vortex Thrust (3-Phase Drive)")
plt.grid(True)
plt.legend()
plt.tight_layout()


# Overlay voltage (one phase) and its derivative alongside thrust

plt.figure(figsize=(12, 6))

# Normalize for comparison
V_A_norm = V_A / V0  # normalized voltage
dV_A_dt_norm = dV_A_dt / np.max(np.abs(dV_A_dt))  # normalized derivative
T_norm = T_total_g / np.max(np.abs(T_total_g))  # normalized thrust

plt.plot(t * 1000, V_A_norm, label='Voltage Phase A (normalized)', color='blue')
plt.plot(t * 1000, dV_A_dt_norm, label='dV/dt Phase A (normalized)', color='red', linestyle='--')
plt.plot(t * 1000, T_norm, label='Total Thrust (normalized)', color='purple', linestyle='-.')

plt.xlabel("Time (ms)")
plt.ylabel("Normalized Value")
plt.title("Overlay of Voltage, dV/dt, and VAM Thrust (Phase A)")
plt.legend()
plt.grid(True)
plt.tight_layout()


import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
t = np.linspace(0, 20e-3, 1000)  # 20 ms total time, 1 kHz sample rate
V0 = 30000  # Peak voltage in volts (e.g., 30kV)
f = 50  # Frequency in Hz

# Generate a sawtooth waveform (simulate voltage)
from scipy.signal import sawtooth
voltage = V0 * (0.5 * sawtooth(2 * np.pi * f * t, width=0.99) + 0.5)

# Derivative of voltage (dV/dt)
dVdt = np.gradient(voltage, t)

# Assume a simple thrust model based on dV/dt with a gain
k_thrust = 1e-6  # Arbitrary gain factor (to match thrust magnitude in grams)
thrust = k_thrust * dVdt  # Thrust in Newtons (assuming units)
thrust_g = thrust * 1000 / 9.81  # Convert Newtons to grams-force

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(t * 1000, voltage / 1000, label='Voltage (kV)', color='blue')
plt.plot(t * 1000, dVdt / 1000, label='dV/dt (kV/ms)', color='red', linestyle='--')
plt.plot(t * 1000, thrust_g, label='Thrust (grams-force)', color='purple', linestyle='-.')
plt.title("Sawtooth Voltage, dV/dt, and Simulated VAM Thrust")
plt.xlabel("Time (ms)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()