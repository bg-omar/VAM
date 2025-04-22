import os
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Define grid
x = np.linspace(-3, 3, 60)
y = np.linspace(-3, 3, 60)
X, Y = np.meshgrid(x, y)

# Avoid division by zero at the origin
epsilon = 1e-5
r2 = X**2 + Y**2 + epsilon
psi = -Y / r2  # Negative dipole (M < 0)

# Uniform flow
U_uniform = np.ones_like(X)
V_uniform = np.zeros_like(Y)

# Dipole flow (vortex doublet)
U_dipole = -(X**2 - Y**2) / r2**2
V_dipole = -(2 * X * Y) / r2**2

# Superposed flow
U_total = U_uniform + U_dipole
V_total = V_uniform + V_dipole

# Create subplots
fig = plt.figure(figsize=(15, 5))
gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 1])

# Plot 1: Uniform flow
ax0 = plt.subplot(gs[0])
ax0.streamplot(X, Y, U_uniform, V_uniform, color='black', density=1.0, linewidth=1)
ax0.set_title("Uniforme parallelstroming")
ax0.set_aspect('equal')
ax0.set_xticks([])
ax0.set_yticks([])

# Plot 2: Dipole flow
ax1 = plt.subplot(gs[1])
ax1.streamplot(X, Y, U_dipole, V_dipole, color='black', density=1.2, linewidth=1)
ax1.axhline(0, color='black', linewidth=1)
ax1.set_title("Dipool stroming")
ax1.set_aspect('equal')
ax1.set_xticks([])
ax1.set_yticks([])

# Plot 3: Combined flow
ax2 = plt.subplot(gs[2])
ax2.streamplot(X, Y, U_total, V_total, color='black', density=1.2, linewidth=1)
# Cilinder
circle = plt.Circle((0, 0), 1, color='black', fill=False, linewidth=1.5)
ax2.add_patch(circle)

ax2.axhline(0, color='black', linewidth=1)
ax2.set_title("Gecombineerde stroming")
ax2.set_aspect('equal')
ax2.set_xticks([])
ax2.set_yticks([])

plt.tight_layout()


import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

plt.show()