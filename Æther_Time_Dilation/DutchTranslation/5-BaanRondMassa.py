import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_title("Cirkelvormige baan rond massa M met gecombineerde tijdsdilatatie", fontsize=13)

# Draw central mass
mass_radius = 0.5
mass = plt.Circle((0, 0), mass_radius, color='black')
ax.add_patch(mass)
ax.text(0, 0, 'M', color='white', fontsize=12, ha='center', va='center')

# Orbital path
orbital_radius = 4
orbit = plt.Circle((0, 0), orbital_radius, color='gray', linestyle='--', fill=False)
ax.add_patch(orbit)

# Vortex position
angle = np.pi / 4
vx = orbital_radius * np.cos(angle)
vy = orbital_radius * np.sin(angle)
vortex = plt.Circle((vx, vy), 0.6, color='lightblue', ec='black', linewidth=2)
ax.add_patch(vortex)
ax.plot(vx + 0.4, vy, 'ro', markersize=10)
ax.text(vx, vy - 1, 'Wervelklok', ha='center', fontsize=11)

# Velocity vectors
# Tangential velocity (vorb)
vt_x = -np.sin(angle)
vt_y = np.cos(angle)
ax.arrow(vx, vy, vt_x, vt_y, head_width=0.2, head_length=0.3,
         fc='green', ec='green', linewidth=2)
ax.text(vx + vt_x + 0.3, vy + vt_y, r'$\vec{v}_{\mathrm{orb}}$', color='green', fontsize=12)

# Radial æther inflow (vg)
vg_x = -np.cos(angle)
vg_y = -np.sin(angle)
ax.arrow(vx, vy, vg_x, vg_y, head_width=0.2, head_length=0.3,
         fc='deepskyblue', ec='deepskyblue', linewidth=2)
ax.text(vx + vg_x - 0.5, vy + vg_y, r'$\vec{v}_g$', color='deepskyblue', fontsize=12)

# Relative velocity (vrel) vector (hypotenuse)
vrel_x = vt_x + vg_x
vrel_y = vt_y + vg_y
ax.arrow(vx, vy, vrel_x, vrel_y, head_width=0.2, head_length=0.3,
         fc='purple', ec='purple', linewidth=2)
ax.text(vx + vrel_x + 0.2, vy + vrel_y, r'$\vec{v}_{\mathrm{rel}}$', color='purple', fontsize=12)

# Formula box
formula = r"$v_{\mathrm{rel}} = \sqrt{v_{\mathrm{orb}}^2 + v_g^2}$" + "\n" + \
          r"$\frac{d\tau}{dt} = \sqrt{1 - \frac{v_{\mathrm{rel}}^2}{c^2}}$"
ax.text(-6, -6.5, formula, fontsize=12, ha='left', va='top', bbox=dict(facecolor='white', alpha=0.7))

# Caption
plt.figtext(0.5, 0.01,
            "Een vortex in een cirkelvormige baan ervaart gecombineerde tijdsdilatatie door orbitaal- en ætherstroming.",
            wrap=True, horizontalalignment='center', fontsize=11)

import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()