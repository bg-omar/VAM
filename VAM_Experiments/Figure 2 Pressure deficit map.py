# Re-import necessary packages after code execution environment reset
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Parameters
grid_size = 200
radius = 0.1  # meters
max_velocity = 200  # m/s, at the ring
rho_ae = 7e-7  # kg/m^3

# Create 2D grid
x = np.linspace(-0.2, 0.2, grid_size)
y = np.linspace(-0.2, 0.2, grid_size)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

# Velocity profile: peak at ring radius, falling off away from it
velocity = max_velocity * np.exp(-((R - radius) ** 2) / (2 * (0.03)**2))

# Bernoulli pressure: P = P0 - 1/2 rho v^2
delta_P = -0.5 * rho_ae * velocity**2

# Smooth for visualization
delta_P_smooth = gaussian_filter(delta_P, sigma=2)

# Plot
fig, ax = plt.subplots(figsize=(6, 5))
contour = ax.contourf(X, Y, delta_P_smooth * 1e6, levels=30, cmap="coolwarm")  # µPa
cbar = plt.colorbar(contour)
cbar.set_label("Pressure Deficit [μPa]")
ax.set_title("Figure 2: Pressure Deficit Map Above Coil")
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_aspect('equal')
plt.tight_layout()
net_rotating_swirl_filename = "Figure 2_Pressure Deficit Map Above Coil.png"
plt.savefig(net_rotating_swirl_filename, dpi=150)
plt.show()
