import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the trefoil knot (swirling knot) centered around origin
theta = np.linspace(0, 2 * np.pi, 500)
x_knot = (2 + np.cos(3 * theta)) * np.cos(2 * theta)
y_knot = (2 + np.cos(3 * theta)) * np.sin(2 * theta)
z_knot = np.sin(3 * theta)

# Define the polar thread: spiral through center of the knot
t_thread = np.linspace(-2 * np.pi, 2 * np.pi, 400)
x_thread = 0.2 * np.cos(t_thread)
y_thread = 0.2 * np.sin(t_thread)
z_thread = t_thread / np.pi

# Begin plotting
fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})
# Define view angles for each subplot
view_angles = [
    (30, 40),    # Angled view: Elevation, Azimuth
    (90, 0),    # Angled view
    (0, 20),    # Angled view
]
titles = ["Kid 1", "Kid 2", "ManBearPig"]

for ax, (elev, azim), title in zip(axes.flatten(), view_angles, titles):
    # Plot the trefoil knot
    ax.plot3D(x_knot, y_knot, z_knot, color='navy', lw=2, label='Swirling Vortex Knot (Fermion)')

    # Plot the helicity-driven axial vortex thread (through core)
    ax.plot3D(x_thread, y_thread, z_thread, color='darkorange', lw=2.5, label='Polar Vortex Thread (Time Flow)')

    # Add arrow to show helicity direction
    ax.quiver(0, 0, 0, 0, 0, 1.5, color='red', arrow_length_ratio=0.1)
    ax.text(0.2, 0.6, 1.6, 'Helicity → Time', fontsize=9, color='red')

    # Label points
    ax.text(0, -0.3, 3, 'Axial Thread\n(through knot center)', fontsize=10, ha='center')
    ax.text(-2, 2, -2.5, 'Swirling Knot\n(Core $C_e$)', fontsize=10)

    # Axis settings
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-3, 3])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('Knot with Threaded Polar Flow')

    # Set view angle
    ax.view_init(elev=elev, azim=azim)
    ax.legend()
    plt.tight_layout()




# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.pdf"
plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()