import matplotlib.pyplot as plt
import numpy as np

# Set up figure with 2 subplots: one for schematic, one for graph
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Tijdbevriezing bij de gebeurtenishorizon", fontsize=15)

# --- Left: Schematic view of æther infall towards black hole ---
ax1.set_aspect('equal')
ax1.set_xlim(-6, 6)
ax1.set_ylim(-6, 6)
ax1.set_title("Ætherinstroom richting gebeurtenishorizon")

# Draw Schwarzschild radius (event horizon)
rs = 2
horizon = plt.Circle((0, 0), rs, color='black', alpha=0.8)
ax1.add_patch(horizon)
ax1.text(0, 0, 'r = rs', color='white', fontsize=11, ha='center')

# Æther flow arrows pointing inward
radii = np.linspace(3, 5.5, 4)
angles = np.linspace(0, 2 * np.pi, 20, endpoint=False)
for r in radii:
    for theta in angles:
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        dx = -0.4 * np.cos(theta)
        dy = -0.4 * np.sin(theta)
        ax1.arrow(x, y, dx, dy, head_width=0.2, head_length=0.3,
                  fc='deepskyblue', ec='deepskyblue', linewidth=1.5)

# Frozen vortex at horizon
vortex = plt.Circle((rs * np.cos(np.pi / 4), rs * np.sin(np.pi / 4)), 0.6,
                    color='lightblue', ec='black', linewidth=2)
ax1.add_patch(vortex)
ax1.text(rs * np.cos(np.pi / 4), rs * np.sin(np.pi / 4) - 1,
         'ωobs → 0', ha='center', fontsize=11)

ax1.axis('off')

# --- Right: Graph of dτ/dt vs. radius ---
ax2.set_title("dτ/dt versus afstand r tot M")
r_vals = np.linspace(rs + 0.01, 10, 300)
dil_vals = np.sqrt(1 - 2 / r_vals)  # normalized: 2GM = 2, c = 1

ax2.plot(r_vals, dil_vals, color='purple', linewidth=2)
ax2.axvline(rs, color='black', linestyle='--', label='r = rs')
ax2.set_xlabel("r (afstand tot massa M, in eenheden waar rs = 2)")
ax2.set_ylabel(r"$\frac{d\tau}{dt}$")
ax2.set_ylim(0, 1.05)
ax2.grid(True)
ax2.legend()

# Caption
plt.figtext(0.5, 0.01,
            "De klok bij de gebeurtenishorizon stopt: dτ/dt → 0. Dit wordt veroorzaakt door maximale ætherinstroom (vg → c).",
            wrap=True, horizontalalignment='center', fontsize=11)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])


###################################################

import matplotlib.pyplot as plt
import numpy as np

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

# # Caption
# plt.figtext(0.5, 0.01,
#             "Ætherstroming versnelt richting $r_s$, waar de waargenomen rotatie van de klok nul wordt: tijd bevriest.",
#             wrap=True, horizontalalignment='center', fontsize=11)

import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()