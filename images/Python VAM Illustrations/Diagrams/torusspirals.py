import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Define torus parameters
R = 2.0  # Major radius (distance from center to tube center, in XY plane)
r = 0.9 * R  # Minor radius (tube thickness)
num_points = 100  # Resolution of the torus

# Define the toroidal grid
theta = np.linspace(0, 2 * np.pi, num_points)  # Angle around the central ring
phi = np.linspace(0, 2 * np.pi, num_points)  # Angle around the tube
Theta, Phi = np.meshgrid(theta, phi)

# Compute torus coordinates
X = (R + r * np.cos(Phi)) * np.cos(Theta)
Y = (R + r * np.cos(Phi)) * np.sin(Theta)
Z = r * np.sin(Phi)

# Define a helical spiral through the center hole
num_helix_turns = 3  # Number of turns of the spiral
helix_theta = np.linspace(0, 2 * np.pi, num_points * num_helix_turns)  # More resolution
helix_phi = 3 * helix_theta  # Wraps 3 times around r per full revolution of R

# Compute helix on the torus surface
helix_x = (R + r * np.cos(helix_phi)) * np.cos(helix_theta)
helix_y = (R + r * np.cos(helix_phi)) * np.sin(helix_theta)
helix_z = r * np.sin(helix_phi)

# Define additional helices for positions 2-5-8 and 3-6-9
helix_x2 = (R + r * np.cos(helix_phi)) * np.cos(helix_theta + 2 * np.pi / 3)
helix_y2 = (R + r * np.cos(helix_phi)) * np.sin(helix_theta + 2 * np.pi / 3)
helix_z2 = r * np.sin(helix_phi + 2 * np.pi / 3)

helix_x3 = (R + r * np.cos(helix_phi)) * np.cos(helix_theta + 4 * np.pi / 3)
helix_y3 = (R + r * np.cos(helix_phi)) * np.sin(helix_theta + 4 * np.pi / 3)
helix_z3 = r * np.sin(helix_phi + 4 * np.pi / 3)

# Create figure
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot torus surface
ax.plot_surface(X, Y, Z, color='lightblue', alpha=0.05, edgecolor='k')

# Plot helical spiral through the center hole
ax.plot(helix_x, helix_y, helix_z, 'r-', linewidth=2)
ax.plot(helix_x2, helix_y2, helix_z2, 'b-', linewidth=2)
ax.plot(helix_x3, helix_y3, helix_z3, 'g-', linewidth=2)

# Set labels and aspect ratio
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("3 balls in a torus")
ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio

ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-4, 4)

# Identify points where the helix reaches the outer edge
num_labels = 9  # Adjust for different numbers (3, 6, 9, etc.)
for i in range(num_labels):
    index = i * len(helix_theta) // num_labels
    ax.text(helix_x[index], helix_y[index], 0, str(i + 1), color='black', fontsize=12, ha='center', va='center')

# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}1.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()

# Create multiple subplots for different views
fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

# Define view angles for each subplot
view_angles = [
    (90, 90),   # Top view
    (0, 90),    # Side view
    (30, 60)    # Angled view
]

titles = ["Top View", "Side View", "Angled View"]

for ax, (elev, azim), title in zip(axes, view_angles, titles):
    # Plot torus surface
    ax.plot_surface(X, Y, Z, color='lightblue', alpha=0.05, edgecolor='k')

    # Plot helical spirals
    ax.plot(helix_x, helix_y, helix_z, 'g-', linewidth=2)
    ax.plot(helix_x2, helix_y2, helix_z2, 'b-', linewidth=2)
    ax.plot(helix_x3, helix_y3, helix_z3, 'r-', linewidth=2)

    # Set view angle
    ax.view_init(elev=elev, azim=azim)

    # Set limits and labels
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_zlim(-4, 4)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio
    ax.set_title(title)

plt.tight_layout()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()