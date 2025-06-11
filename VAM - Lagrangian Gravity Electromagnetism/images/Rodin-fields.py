import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Constants (arbitrary example values, can be refined based on physical context)
N = 12  # number of turns
mu_0 = 4 * np.pi * 1e-7  # vacuum permeability
I = 1.0  # current in Amps
R = 0.1  # average radius of the polygon (meters)

# Define the spatial grid
x = np.linspace(-5, 5, 10)
y = np.linspace(-5, 5, 10)
z = np.linspace(-5, 5, 10)
X, Y, Z = np.meshgrid(x, y, z)

# Compute r and a
r = np.sqrt(X**2 + Y**2 + Z**2)
a = np.sqrt(X**2 + Y**2)

# Avoid division by zero
r[r == 0] = 1e-12
a[a == 0] = 1e-12

# Compute components of B
prefactor = N * mu_0 * I * r / (4 * (r - R)**2)
Bx = prefactor * ((Z * X) / (a * r) - 24 * Y / a)
By = prefactor * ((Z * Y) / (a * r) - 24 * X / a)
Bz = -prefactor * (a / r)

# Normalize vectors for quiver plot
magnitude = np.sqrt(Bx**2 + By**2 + Bz**2)
Bx_norm = Bx / magnitude
By_norm = By / magnitude
Bz_norm = Bz / magnitude

# Subsample for visualization
stride = 1
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X[::stride,::stride,::stride],
          Y[::stride,::stride,::stride],
          Z[::stride,::stride,::stride],
          Bx_norm[::stride,::stride,::stride],
          By_norm[::stride,::stride,::stride],
          Bz_norm[::stride,::stride,::stride],
          length=0.5, normalize=True)

ax.set_title("3D Vector Field of Rodin Coil Approximation (B Field)")
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
plt.tight_layout()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

plt.show()