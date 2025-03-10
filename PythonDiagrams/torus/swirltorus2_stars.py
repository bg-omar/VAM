import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# Define torus parameters
R = 2.0  # Major radius (distance from center to tube center, in XY plane)
r = 0.9 * R  # Minor radius (tube thickness)
num_points = 72  # Resolution of the torus

# Define the toroidal grid
theta = np.linspace(0, 2 * np.pi, num_points)  # Angle around the central ring
phi = np.linspace(0, 2 * np.pi, num_points)  # Angle around the tube
Theta, Phi = np.meshgrid(theta, phi)

# Compute torus coordinates
X = (R + r * np.cos(Phi)) * np.cos(Theta)
Y = (R + r * np.cos(Phi)) * np.sin(Theta)
Z = r * np.sin(Phi)


# Create figure
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot torus surface
ax.plot_surface(X, Y, Z, color='lightblue', alpha=0.1, edgecolor='k')

# Define a single continuous helix wrapping around the torus
num_helix_turns = 3
helix_theta = np.linspace(0, 8 * np.pi, num_points * num_helix_turns)  # Covers 4 full revolutions
helix_phi = 36 * helix_theta

# Compute the helix on the torus surface
helix_x = (R + r * np.cos(helix_phi)) * np.cos(helix_theta)
helix_y = (R + r * np.cos(helix_phi)) * np.sin(helix_theta)
helix_z = r * np.sin(helix_phi)

# Plot the single continuous helix
ax.plot(helix_x, helix_y, helix_z, 'r-', linewidth=2)


# Identify points where the helix reaches the outer edge
num_labels = 9  # Adjust for different numbers (3, 6, 9, etc.)
for i in range(num_labels):
    index = i * len(helix_theta) // num_labels
    ax.text(4.1*np.cos(helix_theta)[index], 4.1*np.sin(helix_theta)[index], 0, str(i + 1), color='black', fontsize=14, ha='center', va='center')
# Plot helical spiral through the center hole

# Define additional helices for positions 2-5-8 and 3-6-9
helix_x2 = (R + r * np.cos(3 * helix_theta + 2 * np.pi / 3)) * np.cos(helix_theta + 2 * np.pi / 3)
helix_y2 = (R + r * np.cos(3 * helix_theta + 2 * np.pi / 3)) * np.sin(helix_theta + 2 * np.pi / 3)
helix_z2 = r * np.sin(3 * helix_theta + 2 * np.pi / 3)

helix_x3 = (R + r * np.cos(3 * helix_theta + 4 * np.pi / 3)) * np.cos(helix_theta + 4 * np.pi / 3)
helix_y3 = (R + r * np.cos(3 * helix_theta + 4 * np.pi / 3)) * np.sin(helix_theta + 4 * np.pi / 3)
helix_z3 = r * np.sin(3 * helix_theta + 4 * np.pi / 3)
ax.plot(helix_x, helix_y, helix_z, 'r-', linewidth=.5)
ax.plot(helix_x2, helix_y2, helix_z2, 'b-', linewidth=2)
#ax.plot(helix_x3, helix_y3, helix_z3, 'g-', linewidth=2)

# Set labels and aspect ratio
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Torus with rolling Stars")
ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio

ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-4, 4)

plt.tight_layout()
plt.show()
