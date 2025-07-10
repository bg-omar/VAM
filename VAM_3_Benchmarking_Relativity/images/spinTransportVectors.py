import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Trefoil knot parametric centerline (T(2,3))
theta = np.linspace(0, 2 * np.pi, 300)
x = (2 + np.cos(3 * theta)) * np.cos(2 * theta)
y = (2 + np.cos(3 * theta)) * np.sin(2 * theta)
z = np.sin(3 * theta)

# Define swirl vector field S ~ grad(cross(v))
# For visualization, we use a mock precession vector along the knot direction
dx = np.gradient(x)
dy = np.gradient(y)
dz = np.gradient(z)

# Normalize for vector field
magnitude = np.sqrt(dx**2 + dy**2 + dz**2)
ux = dx / magnitude
uy = dy / magnitude
uz = dz / magnitude

# Subsample for clarity
step = 20
x_sub, y_sub, z_sub = x[::step], y[::step], z[::step]
ux_sub, uy_sub, uz_sub = ux[::step], uy[::step], uz[::step]

# Begin plotting
fig, axes = plt.subplots(1, 3, figsize=(18, 6), subplot_kw={'projection': '3d'})
# Define view angles for each subplot
view_angles = [
    (30, 40),    # Angled view: Elevation, Azimuth
    (90, 180),    # Angled view
    (0, 0),    # Angled view
]

for i, (ax, (elev, azim)) in enumerate(zip(axes.flatten(), view_angles)):
    ax.plot(x, y, z, color='blue', label='Trefoil Knot Core  (T(2,3)-configuration)')
    ax.quiver(x_sub, y_sub, z_sub, ux_sub, uy_sub, uz_sub, length=0.5, normalize=True, color='crimson', label='$\vec{S}$ Spin Transport Vector')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-3, 3)
    ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio

    if i == 1:
        ax.set_title('Spin Transport Vector Field Along Swirling Trefoil Knot')
        ax.legend()
        ax.set_zticklabels([])

    if i == 2:
        ax.set_zlim(-2, 2)
        ax.set_xticklabels([])

    ax.view_init(elev=elev, azim=azim)


plt.tight_layout()
plt.subplots_adjust(left=0.03, right=0.97, wspace=0.2)

# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# # plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()