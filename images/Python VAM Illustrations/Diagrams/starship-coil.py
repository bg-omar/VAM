# Re-import necessary libraries since execution state was reset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the base sequence for the star-shaped coil using only 9 points
base_sequence = [1, 5, 9, 4, 8, 3, 7, 2, 6, 1]  # This sequence should only use 9 unique points

# Define number of turns in the coil and spacing in the Z-direction
num_turns = 5  # Number of full cycles up the coil
z_spacing = 0.2  # Distance between layers in the Z-direction

# Define the 9 points evenly spaced around a circle
angles = np.linspace(0, 2 * np.pi, 10)[:-1]  # 9 points in a circular arrangement
positions = {i+1: (np.cos(angle), np.sin(angle)) for i, angle in enumerate(angles)}

# Generate 3D coil wire path using only the 9 points
x_vals, y_vals, z_vals = [], [], []
for turn in range(num_turns):
    z_layer = turn * z_spacing  # Increase height per turn
    for num in base_sequence:
        x, y = positions[num]  # Get (x, y) position from the sequence
        x_vals.append(x)
        y_vals.append(y)
        z_vals.append(z_layer)  # Move up in height with each full loop

# Plot 3D Coil
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot the coil wire path
ax.plot(x_vals, y_vals, z_vals, color='blue', linewidth=2, label="Coil Path")

# Mark each coil point
ax.scatter(x_vals, y_vals, z_vals, color='red', s=40)

# Set labels and title
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Height (Z)")
ax.set_title("3D Star-Shaped Coil Representation (9 Points)", fontsize=14)
ax.legend()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()
