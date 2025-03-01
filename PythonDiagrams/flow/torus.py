import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the torus parameters
num_points = 50  # Resolution of the torus
R = 2.0  # Major radius (distance from center to tube center)
r = 2.0  # Minor radius (tube radius)

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
ax.plot_surface(X, Z, Y, color='lightblue', alpha=0.2, edgecolor='k')

# Set labels and aspect ratio
ax.set_xlabel("X")
ax.set_ylabel("Z")
ax.set_zlabel("Y")
ax.set_title("3D Torus")
ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 5)
ax.plot([-5, 5], [0, 0], [0, 0], 'r-', alpha=0.5, linewidth=2)  # X-axis line
ax.quiver(0, -5, 0, 0, 10, 0, color='g', linewidth=2,  alpha=0.5,arrow_length_ratio=0.2)  # Y-axis line
ax.plot([0, 0], [0, 0], [-5, 5], 'b-',  alpha=0.5,linewidth=2)  # Z-axis line

plt.show()
