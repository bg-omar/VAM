# Re-import necessary libraries since execution state was reset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define grid for 3D plot
theta = np.linspace(0, 2 * np.pi, 100)  # Angular component
r = np.linspace(0, 3, 100)  # Radial component (normalized units)
R, Theta = np.meshgrid(r, theta)  # Create meshgrid

# Define Rc and a0 in normalized units
Rc = 0.2  # Coulomb barrier radius (arbitrary scale)
a0 = 1.0  # Bohr radius (arbitrary scale)

# Define the vortex swirl profile
v_theta = (1 - np.exp(-(R - Rc) / a0)) * (R > Rc)
v_theta[R < Rc] = 0  # Suppress swirl inside Rc

# Convert to Cartesian coordinates for plotting
X = R * np.cos(Theta)
Y = R * np.sin(Theta)
Z = v_theta  # Swirl amplitude

# Create 3D plot with a highlighted blue line at the nodal region
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Surface plot
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.5)

# Define the nodal region (peak swirl amplitude, around r ≈ a0)
node_r = np.full_like(theta, a0)  # Constant radius at a0
node_x = node_r * np.cos(theta)
node_y = node_r * np.sin(theta)
node_z = (1 - np.exp(-(a0 - Rc) / a0)) * np.ones_like(theta)  # Corresponding amplitude

# Plot the nodal ring in blue
ax.plot(node_x, node_y, node_z, color='blue', linewidth=3, label="1s Orbital Node")


# Define a second vortex mode for the 2s orbital
v_theta_2s = (1 - np.exp(-(R - Rc) / a0)) * (1 - 2 * np.exp(-(R - 2*a0) / a0)) * (R > Rc)
v_theta_2s[R < Rc] = 0  # Suppress swirl inside Rc

# Convert to Cartesian coordinates for plotting
Z_2s = v_theta_2s  # Swirl amplitude for 2s orbital

# Create 3D plot with both 1s and 2s orbitals and marked nodes
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Surface plot for 1s orbital (transparent)
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.3, label="1s Orbital")

# Surface plot for 2s orbital (transparent)
ax.plot_surface(X, Y, Z_2s, cmap='plasma', edgecolor='none', alpha=0.3, label="2s Orbital")

# Define the first nodal region (peak swirl amplitude for 1s orbital)
node_x_1s = a0 * np.cos(theta)
node_y_1s = a0 * np.sin(theta)
node_z_1s = (1 - np.exp(-(a0 - Rc) / a0)) * np.ones_like(theta)

# Define the second nodal region (for 2s orbital at ~2a0)
node_x_2s = 2 * a0 * np.cos(theta)
node_y_2s = 2 * a0 * np.sin(theta)
node_z_2s = (1 - np.exp(-(2*a0 - Rc) / a0)) * np.ones_like(theta)

# Plot the 1s nodal ring in blue
ax.plot(node_x_1s, node_y_1s, node_z_1s, color='blue', linewidth=3, label="1s Orbital Node")

# Plot the 2s nodal ring in red
ax.plot(node_x_2s, node_y_2s, node_z_2s, color='red', linewidth=3, label="2s Orbital Node")

# Labels and title
ax.set_xlabel(r'$x$ (normalized units)')
ax.set_ylabel(r'$y$ (normalized units)')
ax.set_zlabel(r'Vortex Swirl Amplitude')
ax.set_title(r'Electron Vortex Swirl (VAM Interpretation of 1s and 2s Orbitals)')

# Add legend
ax.legend()

# Show plot
plt.show()