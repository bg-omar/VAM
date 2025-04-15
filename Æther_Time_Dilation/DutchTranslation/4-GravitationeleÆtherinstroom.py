import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(7, 7))
ax.set_aspect('equal')
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_title("Gravitationele ætherinstroom rond massa M", fontsize=14)

# Draw central mass
mass_radius = 0.5
mass = plt.Circle((0, 0), mass_radius, color='black')
ax.add_patch(mass)
ax.text(0, 0, 'M', color='white', fontsize=12, ha='center', va='center')

# Æther inflow vectors
radii = np.linspace(1.5, 5.5, 5)
angles = np.linspace(0, 2 * np.pi, 20, endpoint=False)

for r in radii:
    for theta in angles:
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        dx = -0.5 * np.cos(theta)
        dy = -0.5 * np.sin(theta)
        ax.arrow(x, y, dx, dy, head_width=0.2, head_length=0.3,
                 fc='deepskyblue', ec='deepskyblue', linewidth=1.5)

# Add example vortex at a radius
r_vortex = 4
vortex_x = r_vortex * np.cos(np.pi / 4)
vortex_y = r_vortex * np.sin(np.pi / 4)
vortex = plt.Circle((vortex_x, vortex_y), 0.6, color='lightblue', ec='black', linewidth=2)
ax.add_patch(vortex)
ax.plot(vortex_x + 0.4, vortex_y, 'ro', markersize=10)
ax.text(vortex_x, vortex_y - 1, 'Wervelklok', ha='center', fontsize=11)

# Æther speed label
ax.text(0, -6.2, r'Æther instroomsnelheid: $v_g(r) = \sqrt{2GM / r}$',
        fontsize=12, ha='center', color='deepskyblue')

# Caption
plt.figtext(0.5, 0.01,
            "Ætherinstroom richting massa M veroorzaakt gravitationele tijdsdilatatie bij de wervelklok.",
            wrap=True, horizontalalignment='center', fontsize=11)

import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()