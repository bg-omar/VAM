import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Create a torus knot (trefoil) as the central vortex structure
phi = np.linspace(0, 2 * np.pi, 300)
theta = 3 * phi  # Trefoil knot: (3, 2) type

# Torus knot parameters
R0 = 2  # major radius
r0 = 0.5  # minor radius

# Parametric equations for the trefoil knot
X_knot = (R0 + r0 * np.cos(theta)) * np.cos(phi)
Y_knot = (R0 + r0 * np.cos(theta)) * np.sin(phi)
Z_knot = r0 * np.sin(theta)

# Define a 3D grid surrounding the knot
grid_size = 30
x = np.linspace(-4, 4, grid_size)
y = np.linspace(-4, 4, grid_size)
z = np.linspace(-4, 4, grid_size)
X, Y, Z = np.meshgrid(x, y, z)

# Compute cylindrical radius r from the axis of symmetry
R_cyl = np.sqrt(X**2 + Y**2)

# Avoid division by zero
R_cyl[R_cyl < 1e-2] = 1e-2

# Define the 3D velocity field: radial + axial components in cylindrical-like fashion
# Use same alpha and a parameters
alpha_val = 0.3
a_val = 1.0
omega_val = 1.0
rho_val = 1.0

# S(r) from vortex structure
S = (-a_val**4 + R_cyl**4 + 4 * a_val**2 * R_cyl**2 * np.log(R_cyl / a_val)) / (2 * R_cyl**4)
dS_dr = np.gradient(S, x, axis=0)

# 3D vector field components (approximated in cylindrical form)
V_r = -R_cyl * S
V_z = Z * (R_cyl * dS_dr + 2 * S)

# Convert cylindrical (V_r) into Cartesian (Vx, Vy)
Vx = V_r * X / R_cyl
Vy = V_r * Y / R_cyl
Vz = V_z

# Normalize for plotting
speed = np.sqrt(Vx**2 + Vy**2 + Vz**2)
Vx_norm = Vx / (speed + 1e-10)
Vy_norm = Vy / (speed + 1e-10)
Vz_norm = Vz / (speed + 1e-10)

# Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Streamlines
skip = (slice(None, None, 4), slice(None, None, 4), slice(None, None, 4))
ax.quiver(X[skip], Y[skip], Z[skip], Vx_norm[skip], Vy_norm[skip], Vz_norm[skip], length=0.3, normalize=True, color='mediumblue', alpha=0.6)

# Plot the trefoil knot
ax.plot3D(X_knot, Y_knot, Z_knot, color='crimson', linewidth=2, label='Vortex Knot')

# Axis formatting
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$z$')
ax.set_title('3D Velocity Field Surrounding a Trefoil Vortex Knot')
ax.legend()
plt.tight_layout()
# ✅ Get the script filename dynamically
script_name = os.path.splitext(os.path.basename(__file__))[0]
# ✅ **Create a Folder for Saving Frames**
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

