import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define cylinder parameters
num_points = 50  # Number of vertical lines
height = 5  # Height of the cylinder
radius = 2.0  # Radius of the cylinder

# Define the grid for cylinder
z = np.linspace(-height / 2, height / 2, num_points)
theta = np.linspace(0, 2 * np.pi, num_points)
Theta, Z = np.meshgrid(theta, z)
X = radius * np.cos(Theta)
Y = radius * np.sin(Theta)

# Create figure
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot cylinder surface
ax.plot_surface(X, Y, Z, color='lightblue', alpha=0.2, edgecolor='k')

# Add vertical lines inside the cylinder
for angle in np.linspace(0, 2 * np.pi, num_points // 5):
    x_line = radius * np.cos(angle)
    y_line = radius * np.sin(angle)
    ax.plot([x_line, x_line], [y_line, y_line], [-height / 2, height / 2], 'k-', linewidth=0.5)

# Set labels and aspect ratio
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Cylinder with Vertical Lines")
ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio

ax.set_xlim(-radius, radius)
ax.set_ylim(-radius, radius)
ax.set_zlim(-height / 2, height / 2)
ax.plot([-radius, radius], [0, 0], [0, 0], 'r-', linewidth=2)  # X-axis line
ax.quiver(0, -radius, 0, 0, 2 * radius, 0, color='g', linewidth=2, arrow_length_ratio=0.2)  # Y-axis arrow
ax.plot([0, 0], [0, 0], [-height / 2, height / 2], 'b-', linewidth=2)  # Z-axis line


# Fill the XY plane with lines inside the cylinder
xy_grid_size = 20  # Number of grid lines inside the cylinder
x_fill = np.linspace(-radius, radius, xy_grid_size)
y_fill = np.linspace(-radius, radius, xy_grid_size)
X_fill, Y_fill = np.meshgrid(x_fill, y_fill)
Z_fill = np.zeros_like(X_fill)  # All lines at Z = 0

# Mask points outside the cylinder
mask = X_fill**2 + Y_fill**2 <= radius**2
X_fill = X_fill[mask]
Y_fill = Y_fill[mask]
Z_fill = Z_fill[mask]

# Plot the filled XY plane
ax.scatter(X_fill, Y_fill, Z_fill, color='k', s=2)

plt.show()
