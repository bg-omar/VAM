# Re-import required libraries due to kernel reset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
script_name = os.path.splitext(os.path.basename(__file__))[0]


# --- Parameters ---
num_magnets = 16
dipole_ring_radius = 1.5
arrow_length = 0.3
offset = 0.1

# --- Dipole Ring Geometry ---
def generate_dipole_ring(radius, invert=False):
    positions = []
    orientations = []

    for i in range(num_magnets):
        phi = 2 * np.pi * i / num_magnets
        x, y, z = radius * np.cos(phi), radius * np.sin(phi), 0.75 if invert else -0.75
        positions.append(np.array([x, y, z]))

        # Define dipole rotation with cosine tilt in Z
        mx = np.cos(2 * phi)
        my = np.sin(2 * phi)
        mz = np.cos(phi)
        m = np.array([mx, my, (-1 if invert else 1) * mz])
        m /= np.linalg.norm(m)
        orientations.append(m)

    return positions, orientations

# --- Rodin Starship Coil Geometry ---
def generate_rodin_starship(R=1.0, r=1.0, num_turns=10, num_points=1000):
    theta = np.linspace(0, num_turns * 2 * np.pi, num_points)
    phi = (2 + 2/5) * theta
    x = (R + r * np.cos(phi)) * np.cos(theta)
    y = (R + r * np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi) * 0.3  # Flatten Z to fit between dipole rings
    return x, y, z

# --- Plotting ---
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Dipole ring (bottom)
bottom_pos, bottom_ori = generate_dipole_ring(dipole_ring_radius, invert=False)
for pos, ori in zip(bottom_pos, bottom_ori):
    start = pos - ori * offset
    ax.quiver(*start, *ori, length=arrow_length, color='blue', linewidth=2, arrow_length_ratio=0.25)

# Dipole ring (top)
top_pos, top_ori = generate_dipole_ring(dipole_ring_radius, invert=True)
for pos, ori in zip(top_pos, top_ori):
    start = pos - ori * offset
    ax.quiver(*start, *ori, length=arrow_length, color='red', linewidth=2, arrow_length_ratio=0.25)

# Starship coil
x, y, z = generate_rodin_starship()
ax.plot(x, y, z, color='black', linewidth=1.5, label='Starship Coil')

# --- Display Settings ---
ax.set_title("Starship Coil Between Vortex–Antivortex Dipole Ring Pair")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)
ax.set_box_aspect([1, 1, 1])
ax.legend()

plt.tight_layout()
plt.tight_layout()
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()
