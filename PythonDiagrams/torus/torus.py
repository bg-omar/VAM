import matplotlib.pyplot as plt
import numpy as np

# Define parameters for the torus
R = 3  # Major radius
r = 1  # Minor radius

# Define the grid for the torus
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, 2 * np.pi, 100)
theta, phi = np.meshgrid(theta, phi)

# Parametric equations for the torus
X = (R + r * np.cos(phi)) * np.cos(theta)
Y = (R + r * np.cos(phi)) * np.sin(theta)
Z = r * np.sin(phi)

# Plot the torus
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, rstride=5, cstride=5, color='blue', alpha=0.7, edgecolor='k')

# Set labels and title
ax.set_title('Torus Diagram', fontsize=14)
ax.set_xlabel('X-axis', fontsize=12)
ax.set_ylabel('Y-axis', fontsize=12)
ax.set_zlabel('Z-axis', fontsize=12)

# Adjust the view
ax.view_init(30, 30)

######################################################################################################

# Update parameters for r = R torus
R = 3  # Major radius
r = R  # Minor radius (equal to major radius for this torus)

# Parametric equations for the horn torus
X = (R + r * np.cos(phi)) * np.cos(theta)
Y = (R + r * np.cos(phi)) * np.sin(theta)
Z = r * np.sin(phi)

# Plot the torus
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, rstride=5, cstride=5, color='blue', alpha=0.25, edgecolor='k')  # 75% transparent

# Set labels and title
ax.set_title('Horn Torus Diagram (r = R)', fontsize=14)
ax.set_xlabel('X-axis', fontsize=12)
ax.set_ylabel('Y-axis', fontsize=12)
ax.set_zlabel('Z-axis', fontsize=12)

# Adjust the view
ax.view_init(30, 30)

######################################################################################################

# Update parameters for R = r = 1 torus
R = 1  # Major radius
r = 1  # Minor radius (equal to major radius for this torus)

# Parametric equations for the horn torus
X = (R + r * np.cos(phi)) * np.cos(theta)
Y = (R + r * np.cos(phi)) * np.sin(theta)
Z = r * np.sin(phi)

# Create a swirl effect by rotating points around the Z-axis as a function of Z
swirl_factor = 2 * np.pi / max(Z.flatten())
X_swirl = X * np.cos(swirl_factor * Z) - Y * np.sin(swirl_factor * Z)
Y_swirl = X * np.sin(swirl_factor * Z) + Y * np.cos(swirl_factor * Z)

# Plot the swirling torus
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X_swirl, Y_swirl, Z, rstride=5, cstride=5, color='blue', alpha=0.25, edgecolor='k')  # 75% transparent

# Set labels and title
ax.set_title('Swirling Horn Torus (R = r = 1, Z-Axis Rotation)', fontsize=14)
ax.set_xlabel('X-axis', fontsize=12)
ax.set_ylabel('Y-axis', fontsize=12)
ax.set_zlabel('Z-axis', fontsize=12)

# Adjust the view
ax.view_init(30, 30)

######################################################################################################

# Reduce the swirling factor and update transparency
swirl_factor = np.pi / max(Z.flatten())  # Half the previous swirling factor

# Apply the reduced swirl effect
X_swirl = X * np.cos(swirl_factor * Z) - Y * np.sin(swirl_factor * Z)
Y_swirl = X * np.sin(swirl_factor * Z) + Y * np.cos(swirl_factor * Z)

# Plot the updated swirling torus
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X_swirl, Y_swirl, Z, rstride=5, cstride=5, color='blue', alpha=0.15, edgecolor='k')  # 85% transparent

# Set labels and title
ax.set_title('Reduced Swirl Horn Torus (R = r = 1, Z-Axis Rotation)', fontsize=14)
ax.set_xlabel('X-axis', fontsize=12)
ax.set_ylabel('Y-axis', fontsize=12)
ax.set_zlabel('Z-axis', fontsize=12)

# Ensure 1:1:1 aspect ratio
ax.set_box_aspect([1, 1, 1])

# Adjust the view
ax.view_init(30, 30)

######################################################################################################

# Plot the updated swirling torus with adjusted axis limits
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X_swirl, Y_swirl, Z, rstride=5, cstride=5, color='blue', alpha=0.15, edgecolor='k')  # 85% transparent

# Set labels and title
ax.set_title('Reduced Swirl Horn Torus (R = r = 1, Z-Axis Rotation)', fontsize=14)
ax.set_xlabel('X-axis', fontsize=12)
ax.set_ylabel('Y-axis', fontsize=12)
ax.set_zlabel('Z-axis', fontsize=12)

# Ensure 1:1:1 aspect ratio and adjust limits for proper scaling
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio for all axes
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-2.0, 2.0)
ax.set_zlim(-2.0, 2.0)

# Adjust the view
ax.view_init(30, 30)

plt.show()
