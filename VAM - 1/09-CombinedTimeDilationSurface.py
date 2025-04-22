import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # gravitational constant, m^3/kg/s^2
M = 5.972e24     # mass of Earth, kg
c = 3.0e8        # speed of light, m/s

# Generate grid of radii (r) and orbital velocities (v)
r = np.linspace(6.4e6, 1.0e8, 200)  # from Earth's radius to far orbit
v = np.linspace(0, 1.0e7, 200)      # orbital velocities up to ~10,000 km/s

R, V = np.meshgrid(r, v)

# Gravitational inflow velocity (vg) and orbital velocity (vorb)
vg = np.sqrt(2 * G * M / R)
vrel = np.sqrt(V**2 + vg**2)  # Combined relative velocity (vector sum)

# Time dilation factor: dτ/dt = sqrt(1 - v_rel^2 / c^2)
time_dilation = np.sqrt(1 - (vrel**2) / c**2)
time_dilation = np.clip(time_dilation, 0, 1)  # prevent complex values

# Create a 3D surface plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(R / 1e6, V / 1e3, time_dilation, cmap='viridis', edgecolor='none')

# Labels and titles
ax.set_title('Gecombineerde Tijdsdilatatie door Ætherinstroom en Orbitale Beweging', fontsize=12)
ax.set_xlabel('Straal vanaf massamiddelpunt (in $10^6$ meter)', fontsize=10)
ax.set_ylabel('Orbitale snelheid (km/s)', fontsize=10)
ax.set_zlabel('dτ/dt (Tijdsdilatatiefactor)', fontsize=10)
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Tijdsdilatatiefactor dτ/dt')

plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()
