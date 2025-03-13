import math
import os
import re
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.pyplot as plt
import numpy as np

num_points = 72  # Resolution of the torus
num_helix_turns = 3  # Number of turns of the spiral
helix_theta = np.linspace(0, 2 * np.pi, num_points * num_helix_turns)  # More resolution


fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})
# Define view angles for each subplot
view_angles = [
    (20, -20),    # Angled view
    (20, -20),    # Angled view
    (20, -20),    # Angled view
    (90, 90),    # Angled view
    (70, -20),    # Angled view
    (10, -20),    # Angled view
]
titles = ["Ring Torus Diagram (R=1.5 > r=1)", "Horn Torus Diagram (R = 1 = r)", "Swindle Torus Diagram (R=1/2 < r=1)", "Swirl Ring Torus", "Swirl Horn Torus", "Swirl Swindle Torus"]
radii = [(1.5, 1), (1, 1), (0.5, 1), (1.5, 1), (1, 1), (0.5, 1)]
rgb = 1

for ax, (elev, azim), title in zip(axes.flatten(), view_angles, titles):
    # Define parameters for the torus
    R, r = radii[rgb - 1]
    # Identify points where the helix reaches the outer edge

    ax.text((R + 0.25)  * np.cos(helix_theta + (4 * math.pi /12))[1], (R + 0.25)  * np.sin(helix_theta + (4 * math.pi /12))[1], 0.125, str("R"), color='red', fontsize=24, ha='center', va='center')
    ax.text((R+r ) * np.cos(helix_theta + (5 * math.pi /12))[1], (R+r) * np.sin(helix_theta + (5 * math.pi /12))[1], 0.75, str("r"), color='blue', fontsize=24, ha='center', va='center')

    # Define the grid for the torus
    theta = np.linspace(0, 2 * np.pi, 100)
    t = np.linspace(0, 2 * np.pi, 300)
    phi = np.linspace(0, 2 * np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    # Parametric equations for the horn torus
    X = (R + r * np.cos(phi)) * np.cos(theta)
    Y = (R + r * np.cos(phi)) * np.sin(theta)
    Z = r * np.sin(phi)

    # Create a swirl effect by rotating points around the Z-axis as a function of Z
    swirl_factor = 1/12 * np.pi / max(Z.flatten())
    X_swirl = X * np.cos(swirl_factor * Z) - Y * np.sin(swirl_factor * Z)
    Y_swirl = X * np.sin(swirl_factor * Z) + Y * np.cos(swirl_factor * Z)
    # Define a helical spiral through the center hole
    num_helix_turns = 1  # Number of turns of the spiral
    helix_theta = np.linspace(0, num_helix_turns * 2 * np.pi, num_points * num_helix_turns)  # More resolution
    helix_phi = 3  * helix_theta  # Wraps 3 times around r per full revolution of R

    # Compute helix on the torus surface
    helix_x = (R + r * np.cos(helix_phi)) * np.cos(helix_theta)
    helix_y = (R + r * np.cos(helix_phi)) * np.sin(helix_theta)
    helix_z = r * np.sin(helix_phi)
    RX = (R + .01*r * np.cos(phi)) * np.cos(theta)
    RY = (R + .01*r * np.cos(phi)) * np.sin(theta)
    RZ = .03*r * np.sin(phi)

    rZ =  (r + .01*r * np.cos(phi)) * np.cos(theta)
    rY =  R+(r - .01*r * np.cos(phi)) * np.sin(theta)
    rX =  .03*r * np.sin(phi)

    r2Y =  -R+(r - .01*r * np.cos(phi)) * np.sin(theta)
    # Define the trefoil knot

    trefoil_x = np.sin(t) + 2 * np.sin(2 * t)
    trefoil_y = np.cos(t) - 2 * np.cos(2 * t)
    trefoil_z = -np.sin(3 * t)
    # Plot the torus
    if rgb < 4:
        ax.plot_surface(X_swirl, Y_swirl, Z, rstride=5, cstride=5, color='lightblue', alpha=0.05, edgecolor='k')
        ax.plot_surface(RX, RY, RZ, rstride=5, cstride=5, color='red', alpha=1, linewidth=2, edgecolor='red', label="Ring Radius")
        ax.plot_surface(rX, rY, rZ, rstride=5, cstride=5, color='blue', alpha=1, linewidth=2, edgecolor='blue', label="Core Radius")
        ax.plot_surface(rX, r2Y, rZ, rstride=5, cstride=5, color='blue', alpha=1, linewidth=2, edgecolor='blue')
    if rgb > 3:
        ax.plot_surface(X_swirl, Y_swirl, Z, rstride=5, cstride=5, color='blue', alpha=0.07, edgecolor='k')  # 85% transparent
        ax.plot(helix_x, helix_y, helix_z, 'b-', linewidth=.75)
    if rgb == 2:
        ax.plot_surface(2*RX, 2*RY, RZ, rstride=5, cstride=5, color='green', alpha=1, linewidth=2, edgecolor='green', label="Classic Electron Radius")
        ax.text((2*R+0.75) * np.cos(helix_theta - (7 * math.pi / 12))[1],
                (2*R+0.75) * np.sin(helix_theta - (7 * math.pi / 12))[1],
                .125, str("R_e"), color='green', fontsize=24,
                ha='center', va='center')

# Plot torus surface
    rgb += 1
    # Set view angle
    ax.view_init(elev=elev, azim=azim)

    # Set limits and labels
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio
    ax.legend()
    ax.set_title(title)


# ✅ Get the script filename dynamically
script_name = os.path.splitext(os.path.basename(__file__))[0]
# ✅ **Create a Folder for Saving Frames**
save_folder = "export"
if not os.path.exists(save_folder):
    os.makedirs(save_folder, exist_ok=True)  # Ensure folder exists

# Generate a unique filename using timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{script_name}_{timestamp}.png"



save_path = os.path.join(save_folder, filename)
plt.savefig(save_path, dpi=150)  # Save image with high resolution

plt.tight_layout()
plt.show()