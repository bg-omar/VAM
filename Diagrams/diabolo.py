import numpy as np
import matplotlib.pyplot as plt

# Define the sphere and cap parameters
r = 1  # Radius of the spherical dome
z_cap = 0.9  # Height at which the dome is capped

# Create the new cap surface at z = z_cap
cap_radius = np.sqrt(r**2 - z_cap**2)  # Radius of the cap at z = z_cap
cap_phi = np.linspace(0, 2*np.pi, 100)
cap_X = cap_radius * np.cos(cap_phi)
cap_Y = cap_radius * np.sin(cap_phi)
cap_Z = np.full_like(cap_X, z_cap)

# Create the full hemisphere surface
theta = np.linspace(0, np.pi/2, 100)  # From bottom to top of the hemisphere
phi = np.linspace(0, 2*np.pi, 100)  # Full rotation around z-axis

theta, phi = np.meshgrid(theta, phi)
X = r * np.sin(theta) * np.cos(phi)
Y = r * np.sin(theta) * np.sin(phi)
Z = r * np.cos(theta)

# Mask out values above the cap
mask = Z >= z_cap
X_masked, Y_masked, Z_masked = X[~mask], Y[~mask], Z[~mask]

# Define the mirrored dome's position
z_mirror_base = 1.1  # The bottom of the mirrored dome
z_mirror_top = 2.0   # The top of the mirrored dome

# Create the new mirrored hemisphere surface
theta_mirror = np.linspace(0, np.pi/2, 100)  # From bottom to top
phi_mirror = np.linspace(0, 2*np.pi, 100)  # Full rotation around z-axis

theta_mirror, phi_mirror = np.meshgrid(theta_mirror, phi_mirror)
X_mirror = r * np.sin(theta_mirror) * np.cos(phi_mirror)
Y_mirror = r * np.sin(theta_mirror) * np.sin(phi_mirror)
Z_mirror = z_mirror_top - r * np.cos(theta_mirror)  # Mirrored position

# Define the cap for the mirrored dome at z = z_mirror_base
cap_radius_mirror = np.sqrt(r**2 - (z_mirror_top - z_mirror_base)**2)
cap_X_mirror = cap_radius_mirror * np.cos(cap_phi)
cap_Y_mirror = cap_radius_mirror * np.sin(cap_phi)
cap_Z_mirror = np.full_like(cap_X_mirror, z_mirror_base)

# Apply downward shift to entire structure
z_shift = -1
Z_masked_shifted = Z_masked + z_shift
cap_Z_shifted = cap_Z + z_shift
Z_mirror_shifted = Z_mirror + z_shift
cap_Z_mirror_shifted = cap_Z_mirror + z_shift
base_Z_shifted = np.zeros_like(cap_X) + z_shift
base_Z_mirror_shifted = np.full_like(cap_X, z_mirror_top + z_shift)

from matplotlib.colors import Normalize
# Plot the updated domes with corrected upward diagonal inward-pointing arrows for the top dome's South pole
# Define the base circles at z = -1 and z = 1 with radius 1
base_radius = 1  # Adjusted to full radius

# Generate the base circles at z = -1 and z = 1
base_phi = np.linspace(0, 2*np.pi, 200)
base_X = base_radius * np.cos(base_phi)
base_Y = base_radius * np.sin(base_phi)
base_Z_bottom = np.full_like(base_X, -1)  # Bottom circle at z = -1
base_Z_top = np.full_like(base_X, 1)  # Top circle at z = 1

# Plot the updated domes with full-radius base circles
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot shifted original hemisphere (now moved down)
ax.scatter(X_masked, Y_masked, Z_masked_shifted, color='lightblue', alpha=0.6, s=0.5)
ax.plot(cap_X, cap_Y, cap_Z_shifted, color='r', linewidth=2)

# Plot shifted mirrored hemisphere (now moved down)
ax.scatter(X_mirror, Y_mirror, Z_mirror_shifted, color='lightblue', alpha=0.6, s=0.5)
ax.plot(cap_X_mirror, cap_Y_mirror, cap_Z_mirror_shifted, color='blue', linewidth=2)

# Draw the updated base circles at z = -1 and z = 1
ax.plot(base_X, base_Y, base_Z_bottom, color='darkblue', linewidth=2)  # Bottom base (South pole)
ax.plot(base_X, base_Y, base_Z_top, color='red', linewidth=2)  # Top base (North pole)
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}1.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot shifted original hemisphere (now moved down)
ax.scatter(X_masked, Y_masked, Z_masked_shifted, color='lightblue', alpha=0.6, s=0.5)
ax.plot(cap_X, cap_Y, cap_Z_shifted, color='r', linewidth=2)

# Plot shifted mirrored hemisphere (now moved down)
ax.scatter(X_mirror, Y_mirror, Z_mirror_shifted, color='lightblue', alpha=0.6, s=0.5)
ax.plot(cap_X_mirror, cap_Y_mirror, cap_Z_mirror_shifted, color='blue', linewidth=2)

# Draw the updated base circles at z = -1 and z = 1
ax.plot(base_X, base_Y, base_Z_bottom, color='darkblue', linewidth=2)  # Bottom base (South pole)
ax.plot(base_X, base_Y, base_Z_top, color='red', linewidth=2)  # Top base (North pole)
# Add magnetic field arrows
num_arrows = 12  # Number of arrows for field visualization
# Magnetic field visualization (corrected for top dome)
for i in range(num_arrows):
    angle = 2 * np.pi * i / num_arrows
    x_start = r * np.cos(angle)
    y_start = r * np.sin(angle)
    ax.quiver(x_start, y_start, z_shift, 0, 0, 0.4, color='blue', arrow_length_ratio=0.2)  # Blue for bottom dome
    x_end = (cap_radius - 0.05) * np.cos(angle)
    y_end = (cap_radius - 0.05) * np.sin(angle)
    ax.quiver(x_end, y_end, z_cap + z_shift, -0.2*x_end, -0.2*y_end, -0.2, color='red', arrow_length_ratio=0.2)  # Red for bottom dome

for i in range(num_arrows):
    angle = 2 * np.pi * i / num_arrows
    x_start = (cap_radius_mirror - 0.05) * np.cos(angle)
    y_start = (cap_radius_mirror - 0.05) * np.sin(angle)
    ax.quiver(x_start, y_start, z_mirror_base + z_shift, -0.2*x_start, -0.2*y_start, 0.2, color='blue', arrow_length_ratio=0.2)  # Upward diagonal inward arrows for top dome
    x_end = r * np.cos(angle)
    y_end = r * np.sin(angle)
    ax.quiver(x_end, y_end, z_mirror_top + z_shift, 0, 0, -0.4, color='red', arrow_length_ratio=0.2)  # Now red for mirrored dome

# Corrected Pole Labels (now properly switched)
ax.text(0, 0, z_cap + z_shift + 0.1, "N", color='red', fontsize=12, fontweight='bold')
ax.text(0, 0, z_shift - 0.1, "S", color='blue', fontsize=12, fontweight='bold')
ax.text(0, 0, z_mirror_base + z_shift - 0.1, "S", color='blue', fontsize=12, fontweight='bold')  # Switched position
ax.text(0, 0, z_mirror_top + z_shift + 0.1, "N", color='red', fontsize=12, fontweight='bold')  # Switched position

# Ensure a true 1:1:1 aspect ratio
ax.set_xlim([-r, r])
ax.set_ylim([-r, r])
ax.set_zlim([-1, 1])  # Shifted z-axis range
ax.set_box_aspect([1, 1, 1])  # True aspect ratio

# Labels and title
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
ax.set_title("Mirrored Magnetic Spherical Domes: Top South Pole Arrows Upward Inward")

# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()