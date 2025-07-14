# Reimporting necessary libraries after the state reset
import numpy as np
import matplotlib.pyplot as plt

# Define the grid for the tori
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, 2 * np.pi, 100)
theta, phi = np.meshgrid(theta, phi)

# Define parameters for a spindle vortex torus with an opening along the z-axis (R > r)
R_spindle_open = 3  # Major radius of the spindle torus
r_spindle_open = 1  # Minor radius of the spindle torus

# Parametric equations for the spindle torus with an open z-axis
X_spindle_open = (R_spindle_open + r_spindle_open * np.cos(phi)) * np.cos(theta)
Y_spindle_open = (R_spindle_open + r_spindle_open * np.cos(phi)) * np.sin(theta)
Z_spindle_open = r_spindle_open * np.sin(phi)

# Plot the spindle torus with an open z-axis
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# Plot the spindle torus in blue with 85% transparency
ax.plot_surface(X_spindle_open, Y_spindle_open, Z_spindle_open, rstride=5, cstride=5, color='blue', alpha=0.15, edgecolor='k')

# Set labels and title
ax.set_title('Spindle Vortex Torus with Open z-Axis (R > r)', fontsize=14)
ax.set_xlabel('X-axis', fontsize=12)
ax.set_ylabel('Y-axis', fontsize=12)
ax.set_zlabel('Z-axis', fontsize=12)

# Ensure 1:1:1 aspect ratio
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio for all axes
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)

# Adjust the view angle
ax.view_init(30, 30)
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()

######################################################################################################

# Define parameters for the spindle torus (3R = r) with a swirl on the z-axis
R_spindle_swirl = 1  # Major radius of the spindle torus
r_spindle_swirl = 3  # Minor radius of the spindle torus

# Parametric equations for the spindle torus
X_spindle_swirl = (R_spindle_swirl + r_spindle_swirl * np.cos(phi)) * np.cos(theta)
Y_spindle_swirl = (R_spindle_swirl + r_spindle_swirl * np.cos(phi)) * np.sin(theta)
Z_spindle_swirl = r_spindle_swirl * np.sin(phi)

# Add swirl effect along the z-axis
swirl_factor = np.pi / max(Z_spindle_swirl.flatten())  # Define the swirl factor
X_spindle_swirl_mod = X_spindle_swirl * np.cos(swirl_factor * Z_spindle_swirl) - Y_spindle_swirl * np.sin(swirl_factor * Z_spindle_swirl)
Y_spindle_swirl_mod = X_spindle_swirl * np.sin(swirl_factor * Z_spindle_swirl) + Y_spindle_swirl * np.cos(swirl_factor * Z_spindle_swirl)

# Plot the spindle torus with swirl
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# Plot the swirling spindle torus in blue with 85% transparency
ax.plot_surface(X_spindle_swirl_mod, Y_spindle_swirl_mod, Z_spindle_swirl, rstride=5, cstride=5, color='blue', alpha=0.15, edgecolor='k')

# Set labels and title
ax.set_title('Swirling Spindle Torus (3R = r) with z-Axis Swirl', fontsize=14)
ax.set_xlabel('X-axis', fontsize=12)
ax.set_ylabel('Y-axis', fontsize=12)
ax.set_zlabel('Z-axis', fontsize=12)

# Ensure 1:1:1 aspect ratio
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio for all axes
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)

# Adjust the view angle
ax.view_init(30, 30)
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()

######################################################################################################

# Define the parameters for the spindle torus (3R = r)
R_spindle = 1  # Major radius of the spindle torus
r_spindle = 3  # Minor radius of the spindle torus

# Define the parameters for the horn torus (3R = 3r)
R_horn = 3  # Major radius of the horn torus
r_horn = 3  # Minor radius of the horn torus

# Define the grid for parametric equations
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, 2 * np.pi, 100)
theta, phi = np.meshgrid(theta, phi)

# Parametric equations for the spindle torus
X_spindle = (R_spindle + r_spindle * np.cos(phi)) * np.cos(theta)
Y_spindle = (R_spindle + r_spindle * np.cos(phi)) * np.sin(theta)
Z_spindle = r_spindle * np.sin(phi)

# Parametric equations for the horn torus
X_horn = (R_horn + r_horn * np.cos(phi)) * np.cos(theta)
Y_horn = (R_horn + r_horn * np.cos(phi)) * np.sin(theta)
Z_horn = r_horn * np.sin(phi)

# Plot the tori
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# Plot the spindle torus in blue with 85% transparency
ax.plot_surface(X_spindle, Y_spindle, Z_spindle, rstride=5, cstride=5, color='blue', alpha=0.15, edgecolor='k')

# Plot the horn torus in red with 90% transparency
ax.plot_surface(X_horn, Y_horn, Z_horn, rstride=5, cstride=5, color='red', alpha=0.10, edgecolor='k')

# Set labels and title
ax.set_title('Spindle Torus (3R = r) and Horn Torus (3R = 3r)', fontsize=14)
ax.set_xlabel('X-axis', fontsize=12)
ax.set_ylabel('Y-axis', fontsize=12)
ax.set_zlabel('Z-axis', fontsize=12)

# Ensure 1:1:1 aspect ratio
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio for all axes
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)
ax.set_zlim(-15, 15)

# Adjust the view angle
ax.view_init(30, 30)

# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}3.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()


