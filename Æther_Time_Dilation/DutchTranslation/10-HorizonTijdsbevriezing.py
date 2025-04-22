import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_title("Tijdbevriezing bij de gebeurtenishorizon", fontsize=14)

# Draw event horizon (black hole boundary)
rs = 2
event_horizon = plt.Circle((0, 0), rs, color='black', alpha=0.6)
ax.add_patch(event_horizon)
ax.text(0, 0, 'r = $r_s$', color='white', fontsize=12, ha='center', va='center')

# Draw æther inflow vectors toward horizon
radii = np.linspace(rs + 0.5, 5.5, 4)
angles = np.linspace(0, 2 * np.pi, 24, endpoint=False)
for r in radii:
    for theta in angles:
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        dx = -0.6 * np.cos(theta)
        dy = -0.6 * np.sin(theta)
        ax.arrow(x, y, dx, dy, head_width=0.15, head_length=0.2,
                 fc='deepskyblue', ec='deepskyblue', linewidth=1.2)

# Frozen vortex at horizon
theta = np.pi / 3
x_vortex = rs * np.cos(theta)
y_vortex = rs * np.sin(theta)
vortex = plt.Circle((x_vortex, y_vortex), 0.5, color='lightblue', ec='black', linewidth=2)
ax.add_patch(vortex)
ax.plot(x_vortex + 0.4, y_vortex, 'ro', markersize=10)
ax.text(x_vortex, y_vortex + 0.6, 'Bevroren wervel', ha='center', fontsize=11)

# Rotation arrow - omega = 0
ax.text(x_vortex + 0.6, y_vortex - 0.1, r'$\omega_{\mathrm{obs}} = 0$', fontsize=12, color='black')

# Inset: graph of dτ/dt vs r
inset_ax = fig.add_axes([0.65, 0.15, 0.28, 0.25])
r = np.linspace(rs + 0.01, 10, 300)
dil = np.sqrt(1 - rs * 2 / r)
inset_ax.plot(r, dil, color='purple')
inset_ax.set_title(r'$\frac{d\tau}{dt}$ vs $r$', fontsize=10)
inset_ax.set_xlabel(r'$r$', fontsize=8)
inset_ax.set_ylabel(r'$\frac{d\tau}{dt}$', fontsize=8)
inset_ax.grid(True)
inset_ax.set_xlim(rs, 10)
inset_ax.set_ylim(0, 1)

import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()