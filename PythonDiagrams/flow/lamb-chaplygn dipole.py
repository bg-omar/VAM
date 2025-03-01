import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the vortex parameters
num_rings = 10  # Number of stacked rings
num_points = 100  # Points per ring
height = 5  # Height of the vortex
radius = np.linspace(1, 0.3, num_rings)  # Decreasing radius for cone shape

# Define helical streamlines
theta = np.linspace(0, 4 * np.pi, num_points)  # Spiral turns
z_helix = np.linspace(0, height, num_points)
r_helix = np.linspace(1, 0.3, num_points)
x_helix = r_helix * np.cos(theta)
y_helix = r_helix * np.sin(theta)

# Create figure
fig = plt.figure(figsize=(7, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot stacked vortex rings
for i in range(num_rings):
    theta_ring = np.linspace(0, 2 * np.pi, num_points)
    x_ring = radius[i] * np.cos(theta_ring)
    y_ring = radius[i] * np.sin(theta_ring)
    z_ring = np.full_like(theta_ring, i * (height / num_rings))
    ax.plot(x_ring, y_ring, z_ring, 'o-', markersize=2, alpha=0.6, color='teal')

# Plot helical streamline
ax.plot(x_helix, y_helix, z_helix, 'r--', linewidth=2)

# Set labels and aspect ratio
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("3D Vortex Structure")
ax.set_box_aspect([1,1,2])

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Define the vortex parameters
num_rings = 10  # Number of stacked rings
num_points = 100  # Points per ring
height = 5  # Height of the vortex
radius = np.linspace(1, 0.8, num_rings)  # Varying radius for curvature
curve_factor = 1.5  # Adjust curvature

# Define curved helical streamlines
theta = np.linspace(0, 4 * np.pi, num_points)  # Spiral turns
z_helix = np.linspace(0, height, num_points)
r_helix = np.linspace(1, 0.8, num_points)
x_helix = r_helix * np.cos(theta) + curve_factor * np.sin(z_helix / height * np.pi)
y_helix = r_helix * np.sin(theta)

# Create figure
fig = plt.figure(figsize=(7, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot stacked vortex cylinders
for i in range(num_rings):
    theta_ring = np.linspace(0, 2 * np.pi, num_points)
    x_ring = radius[i] * np.cos(theta_ring) + curve_factor * np.sin(i / num_rings * np.pi)
    y_ring = radius[i] * np.sin(theta_ring)
    z_ring = np.full_like(theta_ring, i * (height / num_rings))
    ax.plot(x_ring, y_ring, z_ring, 'o-', markersize=2, alpha=0.6, color='teal')

    # Add cylindrical surfaces
    verts = [list(zip(x_ring, y_ring, z_ring))]
    ax.add_collection3d(Poly3DCollection(verts, alpha=0.3, color='lightblue'))

# Plot helical streamline
ax.plot(x_helix, y_helix, z_helix, 'r--', linewidth=2)

# Set labels and aspect ratio
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Curved 3D Vortex Structure with Cylinders")
ax.set_box_aspect([1,1,2])

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# Define the vortex parameters
num_rings = 20  # More rings for a smoother tube
num_points = 100  # Points per ring
height = 5  # Height of the vortex
radius = np.linspace(1, 0.8, num_rings)  # Varying radius for curvature
curve_factor = 1.5  # Adjust curvature

# Define curved helical streamlines
theta = np.linspace(0, 4 * np.pi, num_points)  # Spiral turns
z_helix = np.linspace(0, height, num_points)
r_helix = np.linspace(1, 0.8, num_points)
x_helix = r_helix * np.cos(theta) + curve_factor * np.sin(z_helix / height * np.pi)
y_helix = r_helix * np.sin(theta)

# Create figure
fig = plt.figure(figsize=(7, 7))  # Set equal aspect ratio
ax = fig.add_subplot(111, projection='3d')

# Generate the tube structure
for i in range(num_rings - 1):
    theta_ring = np.linspace(0, 2 * np.pi, num_points)
    x_ring1 = radius[i] * np.cos(theta_ring) + curve_factor * np.sin(i / num_rings * np.pi)
    y_ring1 = radius[i] * np.sin(theta_ring)
    z_ring1 = np.full_like(theta_ring, i * (height / num_rings))

    x_ring2 = radius[i + 1] * np.cos(theta_ring) + curve_factor * np.sin((i + 1) / num_rings * np.pi)
    y_ring2 = radius[i + 1] * np.sin(theta_ring)
    z_ring2 = np.full_like(theta_ring, (i + 1) * (height / num_rings))

    verts = [list(zip(x_ring1, y_ring1, z_ring1)) + list(zip(x_ring2, y_ring2, z_ring2))]
    ax.add_collection3d(Poly3DCollection(verts, alpha=0.5, color='lightblue'))

# Plot helical streamline
ax.plot(x_helix, y_helix, z_helix, 'r--', linewidth=2)

# Set labels and aspect ratio
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Curved 3D Vortex Tube Structure")
ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio

plt.show()