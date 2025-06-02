import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Æther bubble with vortex core: radial pressure profile
r = np.linspace(1e-16, 5e-15, 500)
r_c = 1.409e-15
rho_ae = 3.893e18
Gamma = 2 * np.pi * r_c * 1.093e6
Omega = Gamma / (2 * np.pi * r_c**2)

pressure = np.zeros_like(r)

for i in range(len(r)):
    if r[i] < r_c:
        v_theta = Omega * r[i]
    else:
        v_theta = Gamma / (2 * np.pi * r[i])
    pressure[i] = 0.5 * rho_ae * v_theta**2


# Pressure drop centered at core
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(r * 1e15, pressure / 1e9, color='darkblue', lw=2)
ax.axvline(1.409e-15 * 1e15, color='red', linestyle='--', label='Core radius $r_c$')
ax.set_xlabel("Radial Distance $r$ (fm)")
ax.set_ylabel("Pressure $P$ (GPa)")
ax.set_title("Pressure Profile Around a Vortex Core in Æther")
ax.grid(True)
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()



# Draw vortex core + spherical shell
fig2, ax2 = plt.subplots(figsize=(6, 6))
core = patches.Circle((0, 0), radius=.5, color='red', label='Vortex Core')
bubble = patches.Circle((0, 0), radius=5, fill=False, linestyle='--', linewidth=2, label='Æther Equilibrium Shell')
ax2.add_patch(core)
ax2.add_patch(bubble)
ax2.set_xlim(-6, 6)
ax2.set_ylim(-6, 6)
ax2.set_aspect('equal')
ax2.set_title("Vortex Knot Surrounded by Ætheric Pressure Shell")
ax2.legend(loc='upper right')
ax2.axis('off')

plt.tight_layout()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}2.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()


# Trefoil knot parametric equations
theta = np.linspace(0, 2 * np.pi, 1000)
x = (2 + np.cos(3 * theta)) * np.cos(2 * theta)
y = (2 + np.cos(3 * theta)) * np.sin(2 * theta)
z = np.sin(3 * theta)

# === Ætheric Shell ===
R_eq = 9
u_sphere = np.linspace(0, 2 * np.pi, 60)
v_sphere = np.linspace(0, np.pi, 30)
xs = R_eq * np.outer(np.cos(u_sphere), np.sin(v_sphere))
ys = R_eq * np.outer(np.sin(u_sphere), np.sin(v_sphere))
zs = R_eq * np.outer(np.ones(np.size(u_sphere)), np.cos(v_sphere))

# === Horn Torus: R = r = a_0 ===
a_0 = 0.5 * R_eq
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, 2 * np.pi, 60)
u, v = np.meshgrid(u, v)
x_torus = a_0 * (1 + np.cos(v)) * np.cos(u)
y_torus = a_0 * (1 + np.cos(v)) * np.sin(u)
phi = (1 + np.sqrt(5)) / 2  # golden ratio
z_torus = a_0 * phi * np.sin(v)


scale_factor = 5e-2
x_knot_scaled = x * scale_factor
y_knot_scaled = y * scale_factor
z_knot_scaled = z * scale_factor

# Zoomed offset
offset = 4
x_zoom = x + offset
y_zoom = y + offset
z_zoom = z + offset

# Generate equilibrium line (spherical radius)
phi = np.linspace(0, 2 * np.pi, 200)
R_eq = 4.5
x_eq = R_eq * np.cos(phi)
y_eq = R_eq * np.sin(phi)
z_eq = np.zeros_like(phi)

# Plot 3D trefoil knot inside spherical shell with equilibrium circle
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot3D(x_knot_scaled, y_knot_scaled, z_knot_scaled, color='red', lw=0.5, label='Trefoil Knot (core, $\\sim 1.4 \\times 10^-15$ m radius)')

ax.plot3D(x_eq, y_eq, z_eq, color='navy', linestyle='--', lw=1.5, label='Bohr Ground State Radius (Bubble Shell $\\sim 1\\times 10^-11$ m)')
ax.plot3D(x_zoom, y_zoom, z_zoom, color='crimson', lw=1.5, label='Zoomed Trefoil Knot')
# Æther shell
#ax.plot_surface(xs, ys, zs, color='lightblue', alpha=0.1, edgecolor='none')
# Horn torus flow (R = r = a_0)
ax.plot_surface(x_torus, y_torus, z_torus, color='purple', alpha=0.05, linewidth=0, label='Bubble Shell $\\sim 1\\times 10^-10$ m')

# Zoom indicator lines (arrows from small to large)
idx1, idx2 = 100, 900  # Two opposing points on the knot
arrow_pairs = [(idx1, 'A'), (idx2, 'B')]

for idx, label in arrow_pairs:
    ax.plot(
        [x_knot_scaled[idx], x_zoom[idx]],
        [y_knot_scaled[idx], y_zoom[idx]],
        [z_knot_scaled[idx], z_zoom[idx]],
        color='black', linestyle='--', linewidth=1
    )



# Semi-transparent spherical shell
u = np.linspace(0, 2 * np.pi, 60)
v = np.linspace(0, np.pi, 30)
xs = R_eq * np.outer(np.cos(u), np.sin(v))
ys = R_eq * np.outer(np.sin(u), np.sin(v))
zs = R_eq * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(xs, ys, zs, color='lightblue', alpha=0.15, edgecolor='none')

ax.set_title("Trefoil Knot and Ætheric Equilibrium Shell")
ax.set_xlim([-6, 6])
ax.set_ylim([-6, 6])
ax.set_zlim([-6, 6])
ax.set_box_aspect([1, 1, 1])
ax.axis('off')
ax.legend(loc='upper left')

plt.tight_layout()

# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}3.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}3.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()