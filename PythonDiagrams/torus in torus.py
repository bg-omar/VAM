# Reimporting necessary libraries after state reset
import os
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt

# Define parameters for the ring torus (R = 4r)
R_ring = 4  # Major radius of the ring torus
r_ring = 1  # Minor radius of the ring torus

# Define parameters for the horn torus (R = 4r)
R_horn = 4  # Major radius of the horn torus
r_horn = 4  # Minor radius of the horn torus

# Define the grid for the tori
theta = np.linspace(0, 2 * np.pi, 100)
phi = np.linspace(0, 2 * np.pi, 100)
theta, phi = np.meshgrid(theta, phi)

# Parametric equations for the ring torus
X_ring = (R_ring + r_ring * np.cos(phi)) * np.cos(theta)
Y_ring = (R_ring + r_ring * np.cos(phi)) * np.sin(theta)
Z_ring = r_ring * np.sin(phi)

# Parametric equations for the horn torus
X_horn = (R_horn + r_horn * np.cos(phi)) * np.cos(theta)
Y_horn = (R_horn + r_horn * np.cos(phi)) * np.sin(theta)
Z_horn = r_horn * np.sin(phi)

# Plot the tori
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# Plot the ring torus in blue with 85% transparency
ax.plot_surface(X_ring, Y_ring, Z_ring, rstride=5, cstride=5, color='blue', alpha=0.15, edgecolor='k')

# Plot the horn torus in red with 90% transparency
ax.plot_surface(X_horn, Y_horn, Z_horn, rstride=5, cstride=5, color='red', alpha=0.10, edgecolor='k')

# Set labels and title
ax.set_title('Ring Torus (R = 4r) and Horn Torus (4R = 4r)', fontsize=14)
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

######################################################################################################

# Define parameters for the spindle torus (2R = r)
R_spindle = 1  # Major radius of the spindle torus
r_spindle = 2  # Minor radius of the spindle torus

# Define parameters for the horn torus (2R = 4r)
R_horn = 2  # Major radius of the horn torus
r_horn = 4  # Minor radius of the horn torus

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
ax.set_title('Spindle Torus (2R = r) and Horn Torus (2R = 4r)', fontsize=14)
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

######################################################################################################

# Define parameters for the spindle torus (3R = r)
R_spindle = 1  # Major radius of the spindle torus
r_spindle = 3  # Minor radius of the spindle torus

# Define parameters for the horn torus (2R = 6r)
R_horn = 2  # Major radius of the horn torus
r_horn = 6  # Minor radius of the horn torus

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
ax.set_title('Spindle Torus (3R = r) and Horn Torus (2R = 6r)', fontsize=14)
ax.set_xlabel('X-axis', fontsize=12)
ax.set_ylabel('Y-axis', fontsize=12)
ax.set_zlabel('Z-axis', fontsize=12)

# Ensure 1:1:1 aspect ratio
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio for all axes
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_zlim(-20, 20)

# Adjust the view angle
ax.view_init(30, 30)

# ✅ Get the script filename dynamically
script_name = os.path.splitext(os.path.basename(__file__))[0]
# ✅ **Create a Folder for Saving Frames**
save_folder = "export"
if not os.path.exists(save_folder):
    os.makedirs(save_folder, exist_ok=True)  # Ensure folder exists

# Generate a unique filename using timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{script_name}_{timestamp}.png"


plt.show()

