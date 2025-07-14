import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation
num_points = 72  # Resolution of the torus
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime



# Set up the figure and 3D axis
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')

# Define torus parameters
R = 2.0  # Major radius
r = 0.9 * R  # Minor radius

# Define the toroidal grid
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, 2 * np.pi, 100)
theta, phi = np.meshgrid(theta, phi)

# Compute torus coordinates
X = (R + r * np.cos(phi)) * np.cos(theta)
Y = (R + r * np.cos(phi)) * np.sin(theta)
Z = r * np.sin(phi)

# Define the helical coil

num_helix_turns = 1
helix_theta = np.linspace(0, 36 * np.pi, 72 * num_helix_turns)

winding_ratio = 3 / (4 * np.pi)  # Ensures exactly 12 windings through the torus
helix_phi = winding_ratio * helix_theta

# Compute helix coordinates
helix_x = (R + r * np.cos(helix_phi)) * np.cos(helix_theta)
helix_y = (R + r * np.cos(helix_phi)) * np.sin(helix_theta)
helix_z = r * np.sin(helix_phi)

# Function to update the frame
def update(frame):
    ax.clear()
    ax.view_init(elev=20, azim=frame * 3)  # Rotate by 3 degrees per frame

    # Plot torus
    ax.plot_surface(X, Y, Z, rstride=5, cstride=5, color='lightblue', alpha=0.08, edgecolor='k')

    # Plot helical coil
    ax.plot(helix_x, helix_y, helix_z, 'r-', linewidth=2)

    # Set limits and labels
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_zlim(-4, 4)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Rotating Torus with Helical Coil")
    ax.set_box_aspect([1, 1, 1])

# Create the animation
num_frames = 120  # Number of frames for smooth rotation
ani = animation.FuncAnimation(fig, update, frames=num_frames, interval=50)

# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.gif"


# Save the animation with a unique name
ani.save(filename, writer='pillow', fps=20)

print(f"Animation saved as: {filename}")




fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})
# Define view angles for each subplot
view_angles = [
    (20, -20),    # Angled view
    (20, -20),    # Angled view
    (20, -20),    # Angled view
    (30, -20),    # Angled view
    (30, -20),    # Angled view
    (30, -20),    # Angled view
]
titles = ["Ring Torus Diagram (R=1.5 > r=1)", "Horn Torus Diagram (R = 1 = r)", "Swindle Torus Diagram (R=1/2 < r=1)", "Swirl Ring Torus", "Swirl Horn Torus", "Swirl Swindle Torus"]
radii = [(1.5, 1), (1, 1), (0.5, 1), (1.5, 1), (1, 1), (0.5, 1)]
rgb = 1

for ax, (elev, azim), title in zip(axes.flatten(), view_angles, titles):
    # Define parameters for the torus
    R, r = radii[rgb - 1]

    def compute_helices(R, r, helix_phi, helix_theta):
        helices = []
        for i in range(3):
            angle = i * np.pi / 1.333
            helix_x = (R + r * np.cos(helix_phi + angle)) * np.cos(helix_theta + angle)
            helix_y = (R + r * np.cos(helix_phi + angle)) * np.sin(helix_theta + angle)
            helix_z = r * np.sin(helix_phi + angle)
            helices.append((helix_x, helix_y, helix_z))
        return helices



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

    # Define helical parameters
    num_helix_turns = 3
    torus_revolutions = 5  # The number of full toroidal cycles before restarting

    # Ensure the helix wraps 12 times inside the torus core
    helix_theta = np.linspace(0, torus_revolutions * 2 * np.pi, 72 * num_helix_turns)  # Covers 9 full torus revolutions

    # Corrected winding ratio to ensure exactly 12 windings
    winding_ratio = 2+2/5
    helix_phi = winding_ratio * helix_theta

    # Define additional helices for 3-phase offset positions
    helix_x2 = (R + r * np.cos(helix_phi)) * np.cos(helix_theta + 2 * np.pi / 3)
    helix_y2 = (R + r * np.cos(helix_phi)) * np.sin(helix_theta + 2 * np.pi / 3)
    helix_z2 = r * np.sin(helix_phi + 2 * np.pi / 3)

    helix_x3 = (R + r * np.cos(helix_phi)) * np.cos(helix_theta + 4 * np.pi / 3)
    helix_y3 = (R + r * np.cos(helix_phi)) * np.sin(helix_theta + 4 * np.pi / 3)
    helix_z3 = r * np.sin(helix_phi + 4 * np.pi / 3)

    # Define Starship Coil variant (Alternative helical wrapping)
    starship_theta = np.linspace(0, 32 * np.pi, num_points * num_helix_turns)
    starship_phi = 8/9 * starship_theta  # Different wrapping ratio for the Starship coil

    starship_x = (R + r * np.cos(starship_phi)) * np.cos(starship_theta)
    starship_y = (R + r * np.cos(starship_phi)) * np.sin(starship_theta)
    starship_z = r * np.sin(starship_phi)

    helices = compute_helices(R, r, helix_phi, helix_theta)

    # Compute helix on the torus surface
    helix_x = (R + r * np.cos(helix_phi)) * np.cos(helix_theta)
    helix_y = (R + r * np.cos(helix_phi)) * np.sin(helix_theta)
    helix_z = r * np.sin(helix_phi)
    RX = (R + .01*r * np.cos(phi)) * np.cos(theta)
    RY = (R + .01*r * np.cos(phi)) * np.sin(theta)
    RZ = .01*r * np.sin(phi)

    rZ =  (r + .01*r * np.cos(phi)) * np.cos(theta)
    rY =  R+(r - .01*r * np.cos(phi)) * np.sin(theta)
    rX =  .01*r * np.sin(phi)

    r2Y =  -R+(r - .01*r * np.cos(phi)) * np.sin(theta)
    # Define the trefoil knot

    trefoil_x = np.sin(t) + 2 * np.sin(2 * t)
    trefoil_y = np.cos(t) - 2 * np.cos(2 * t)
    trefoil_z = -np.sin(3 * t)


    # Identify points where the helix reaches the outer edge
    num_labels = 12  # Adjust for different numbers (3, 6, 9, etc.)
    for i in range(num_labels):
        index = i * len(t) // num_labels
        ax.text(2*R *np.cos(t)[index], 2*R*np.sin(t)[index], 0, str(i + 1), color='black', fontsize=14, ha='center', va='center')
        # Plot helical spiral through the center hole


# Plot the torus
    if rgb ==2 :
        ax.plot_surface(X_swirl, Y_swirl, Z, rstride=5, cstride=5, color='lightblue', alpha=0.08, edgecolor='k')
        # Plot helical Rodin coil windings (3-phase)
        ax.plot(helix_x, helix_y, helix_z, 'r-', linewidth=2, label="Rodin Coil Phase 1")
        ax.plot(helix_x2, helix_y2, helix_z2, 'b-', linewidth=2, label="Rodin Coil Phase 2")
        ax.plot(helix_x3, helix_y3, helix_z3, 'g-', linewidth=2, label="Rodin Coil Phase 3")

    if rgb == 1:
        for i, (helix_x, helix_y, helix_z) in enumerate(helices):
            color = ['r-', 'b-', 'g-'][i % 3]
            width = [1, 1, 1][i % 3]
            ax.plot(helix_x, helix_y, helix_z, color, linewidth=width, alpha=1)

    if rgb == 3:
        # Plot Starship coil winding (alternative Rodin variant)
        ax.plot(starship_x, starship_y, starship_z, 'm-', linewidth=2, label="Starship Coil Variant")
    # if rgb == 6:
    #     ax.plot(R*trefoil_x, R*trefoil_y, R*trefoil_z, 'r-', linewidth=rgb*0.25)


    # Plot torus surface
    rgb += 1
    # Set view angle
    ax.view_init(elev=elev, azim=azim)
    # Create figure
    # Set limits and labels
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    # Show legend
    # ax.legend()
    ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio
    ax.set_title(title)
plt.tight_layout()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()