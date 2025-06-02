# import numpy as np
# import matplotlib.pyplot as plt
#
# # Rooster
# x = np.linspace(-2, 2, 500)
# y = np.linspace(-2, 2, 500)
# X, Y = np.meshgrid(x, y)
# R = np.sqrt(X**2 + Y**2)
#
# # Parameters
# eps = 1e-2  # om singulariteit te vermijden
# cutoff = 0.2  # straal van vortexkern
#
# # Velden
# U = 1 + (X**2 - Y**2) / (R**4 + eps)
# V = (2*X*Y) / (R**4 + eps)
#
# # Set binnenste kern op 0
# U[R < cutoff] = 0
# V[R < cutoff] = 0
#
# # Plot
# plt.figure(figsize=(5,5))
# plt.streamplot(X, Y, U, V, color='black', linewidth=0.8, density=1.5)
# plt.gca().add_patch(plt.Circle((0, 0), cutoff, fill=False, color='black', linewidth=1))
# plt.xlim(-2, 2)
# plt.ylim(-2, 2)
# plt.xlabel('$x/R$')
# plt.ylabel('$y/R$')
# plt.gca().set_aspect('equal')
# plt.tight_layout()
#
# plt.savefig("streamlines_dipole.png", dpi=300)
#

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Define grid
x = np.linspace(-.04, .04, 800)
y = np.linspace(-.04, .04, 800)
X, Y = np.meshgrid(x, y)

# Avoid division by zero at origin
epsilon = 1e-5
R2 = X**2 + Y**2 + epsilon

# Define streamfunction psi = y + y / (x^2 + y^2)
Psi = Y + Y / R2

# Create the plot
fig, ax = plt.subplots(figsize=(12, 12))
contours = ax.contour(X, Y, Psi, levels=22, cmap='inferno')
# # Cilinder
# circle = plt.Circle((0, .004), .001, color='black', fill=False, linewidth=1.5)
# ax.add_patch(circle)
# # Cilinder
# circle2 = plt.Circle((0, -.004), .001, color='black', fill=False, linewidth=1.5)
# ax.add_patch(circle2)
ax.clabel(contours, inline=True, fontsize=8)
ax.set_title(r"Contourplot van $\psi = y + \frac{y}{x^2 + y^2}$")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect('equal')

plt.grid(True)
plt.savefig("streamlines_dipole.png", dpi=300)
plt.show()