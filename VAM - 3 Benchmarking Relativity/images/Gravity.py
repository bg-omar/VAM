import numpy as np
import matplotlib.pyplot as plt

# Physical constants
G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
M = 5.972e24     # Mass of Earth (kg)
r_min = 6.371e6  # Radius of Earth (m)
r_max = 10e6     # Just above surface to visualize field (m)
r = np.linspace(r_min, r_max, 500)

# Inflow velocity (radial æther velocity toward mass center)
v_inflow = np.sqrt((2 * G * M) / r)

# Bernoulli-like pressure gradient (normalized)
pressure_gradient = 1 - (v_inflow**2 / v_inflow[0]**2)

# Plotting the æther inflow velocity and pressure gradient
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(r / 1000, v_inflow, label="Inflow Velocity", color="blue")
plt.ylabel("Velocity (m/s)")
plt.title("Radial Æther Inflow Toward Earth")
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(r / 1000, pressure_gradient, label="Normalized Pressure Gradient", color="red")
plt.xlabel("Radial Distance from Center (km)")
plt.ylabel("Relative Pressure")
plt.title("Bernoulli-Like Pressure Gradient in VAM")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("vam_gravity_model.png", dpi=300)
plt.show()