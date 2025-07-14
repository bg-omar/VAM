import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Define the cylinder parameters
num_points = 100  # Points per ring
height = 2  # Height of the cylinder
radius = 1.0  # Constant radius

# Define the grid for the cylinder
theta = np.linspace(0, 2 * np.pi, num_points)
z = np.linspace(0, height, num_points)
Theta, Z = np.meshgrid(theta, z)
X = radius * np.cos(Theta)
Y = radius * np.sin(Theta)

# Create figure
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot cylinder surface
ax.plot_surface(X, Y, Z, color='lightblue', alpha=0.2, edgecolor='k')

# Set labels and aspect ratio
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("3D")
ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio

ax.set_xlim(-10,10)
ax.set_ylim(-10,10)
ax.set_zlim(-10,10)
ax.plot([-10, 10], [0, 0], [0, 0], 'r-', linewidth=2)  # X-axis line
ax.plot([0, 0], [-10, 10], [0, 0], 'g-', linewidth=2)  # Y-axis line
ax.plot([0, 0], [0, 0], [-10, 10], 'b-', linewidth=2)  # Z-axis line
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()