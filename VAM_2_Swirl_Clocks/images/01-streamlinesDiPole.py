# Æther Vortex Simulation Framework
# Simulates vorticity field, pressure gradients, and local time modulation
import math
import os
import re
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# Grid setup
L = 4.0  # domain size
N = 200  # grid resolution
x = np.linspace(-L, L, N)
y = np.linspace(-L, L, N)
X, Y = np.meshgrid(x, y)

# Vortex parameters (representing an Æther knot)
def vortex_field(x0, y0, gamma, sigma):
    dx = X - x0
    dy = Y - y0
    r2 = dx**2 + dy**2
    factor = gamma / (2 * np.pi * r2) * (1 - np.exp(-r2 / (2 * sigma**2)))
    u = -dy * factor
    v = dx * factor
    return u, v

# Compose multiple vortex knots
vortices = [(-1, 0, 5, 0.3), (1, 0, -5, 0.3)]
U = np.zeros_like(X)
V = np.zeros_like(Y)

for x0, y0, gamma, sigma in vortices:
    u, v = vortex_field(x0, y0, gamma, sigma)
    U += u
    V += v

# Vorticity field (curl of velocity)
dU_dy, dU_dx = np.gradient(U, y, x)
dV_dy, dV_dx = np.gradient(V, y, x)
OMEGA = dV_dx - dU_dy  # scalar vorticity in 2D

# Pressure field (Poisson-like approximation)
P = -0.5 * (U**2 + V**2)

# Local time modulation: tau = 1 / (1 + alpha * omega^2)
alpha = 0.1
tau = 1 / (1 + alpha * OMEGA**2)

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

axs[0, 0].streamplot(x, y, U, V, color='k', density=1.5)
axs[0, 0].set_title("Velocity Field (Streamlines)")

axs[0, 1].streamplot(x, y, -U, -V, color='k', density=1.5)
axs[0, 1].set_title("Velocity Field (Streamlines)")
# cf1 = axs[0, 1].contourf(X, Y, OMEGA, 100, cmap=cm.plasma)
# axs[0, 1].set_title("Vorticity Field")
# fig.colorbar(cf1, ax=axs[0, 1])

cf2 = axs[1, 0].contourf(X, Y, P, 100, cmap=cm.coolwarm)
axs[1, 0].set_title("Pressure Field")
fig.colorbar(cf2, ax=axs[1, 0])

cf3 = axs[1, 1].contourf(X, Y, tau, 100, cmap=cm.viridis)
axs[1, 1].set_title("Local Time Rate ($\\tau$)")
fig.colorbar(cf3, ax=axs[1, 1])

for ax in axs.flat:
    ax.set_aspect('equal')
    ax.set_xlabel("x")
    ax.set_ylabel("y")

plt.tight_layout()

script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()


# Compose two vortices with the same circulation (co-rotating)
vortices = [(-1, 0, 5, 0.3), (1, 0, 5, 0.3)]  # <-- both +5

U = np.zeros_like(X)
V = np.zeros_like(Y)

for x0, y0, gamma, sigma in vortices:
    u, v = vortex_field(x0, y0, gamma, sigma)
    U += u
    V += v

# Vorticity field (curl of velocity)
dU_dy, dU_dx = np.gradient(U, y, x)
dV_dy, dV_dx = np.gradient(V, y, x)
OMEGA = dV_dx - dU_dy  # scalar vorticity in 2D

# Pressure field (Poisson-like approximation)
P = -0.5 * (U**2 + V**2)

# Local time modulation: tau = 1 / (1 + alpha * omega^2)
alpha = 0.1
tau = 1 / (1 + alpha * OMEGA**2)

# Plotting (same as before)
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

axs[0, 0].streamplot(x, y, U, V, color='k', density=1.5)
axs[0, 0].set_title("Velocity Field (Streamlines)")

axs[0, 1].streamplot(x, y, -U, -V, color='k', density=1.5)
axs[0, 1].set_title("Reversed Velocity Field (Streamlines)")

cf2 = axs[1, 0].contourf(X, Y, P, 100, cmap=cm.coolwarm)
axs[1, 0].set_title("Pressure Field")
fig.colorbar(cf2, ax=axs[1, 0])

cf3 = axs[1, 1].contourf(X, Y, tau, 100, cmap=cm.viridis)
axs[1, 1].set_title("Local Time Rate ($\\tau$)")
fig.colorbar(cf3, ax=axs[1, 1])

for ax in axs.flat:
    ax.set_aspect('equal')
    ax.set_xlabel("x")
    ax.set_ylabel("y")

plt.tight_layout()

script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}_same_circulation.png"
plt.savefig(filename, dpi=150)
plt.show()




a = 1.3  # spacing (adjust as you like)
gamma = 5  # circulation
sigma = 0.3  # core size

# Triangle vertices
vortices = [
    ( a, 0,     gamma, sigma),
    (-a/2,  a*np.sqrt(3)/2, gamma, sigma),
    (-a/2, -a*np.sqrt(3)/2, gamma, sigma)
]


U = np.zeros_like(X)
V = np.zeros_like(Y)

for x0, y0, gamma, sigma in vortices:
    u, v = vortex_field(x0, y0, gamma, sigma)
    U += u
    V += v

# Vorticity field (curl of velocity)
dU_dy, dU_dx = np.gradient(U, y, x)
dV_dy, dV_dx = np.gradient(V, y, x)
OMEGA = dV_dx - dU_dy  # scalar vorticity in 2D

# Pressure field (Poisson-like approximation)
P = -0.5 * (U**2 + V**2)

# Local time modulation: tau = 1 / (1 + alpha * omega^2)
alpha = 0.1
tau = 1 / (1 + alpha * OMEGA**2)

# Plotting (same as before)
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

axs[0, 0].streamplot(x, y, U, V, color='k', density=1.5)
axs[0, 0].set_title("Velocity Field (Streamlines)")

axs[0, 1].streamplot(x, y, -U, -V, color='k', density=1.5)
axs[0, 1].set_title("Reversed Velocity Field (Streamlines)")

cf2 = axs[1, 0].contourf(X, Y, P, 100, cmap=cm.coolwarm)
axs[1, 0].set_title("Pressure Field")
fig.colorbar(cf2, ax=axs[1, 0])

cf3 = axs[1, 1].contourf(X, Y, tau, 100, cmap=cm.viridis)
axs[1, 1].set_title("Local Time Rate ($\\tau$)")
fig.colorbar(cf3, ax=axs[1, 1])

for ax in axs.flat:
    ax.set_aspect('equal')
    ax.set_xlabel("x")
    ax.set_ylabel("y")

plt.tight_layout()

script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}_3_same_cores_circulation.png"
plt.savefig(filename, dpi=150)
plt.show()


#
# # Plotting
# fig, axs = plt.subplots(2, 2, figsize=(12, 10))
#
# axs[0, 0].streamplot(x, y, U, V, color='k', density=1.5)
# axs[0, 0].set_title("Snelheidsveld (Stroomlijnen)")
#
# cf1 = axs[0, 1].contourf(X, Y, OMEGA, 100, cmap=cm.plasma)
# axs[0, 1].set_title("Vorticiteitsveld")
# fig.colorbar(cf1, ax=axs[0, 1])
#
# cf2 = axs[1, 0].contourf(X, Y, P, 100, cmap=cm.coolwarm)
# axs[1, 0].set_title("Drukveld")
# fig.colorbar(cf2, ax=axs[1, 0])
#
# cf3 = axs[1, 1].contourf(X, Y, tau, 100, cmap=cm.viridis)
# axs[1, 1].set_title("Lokale tijdsfrequentie ($\\tau$)")
# fig.colorbar(cf3, ax=axs[1, 1])
#
# for ax in axs.flat:
#     ax.set_aspect('equal')
#     ax.set_xlabel("x")
#     ax.set_ylabel("y")
#
# plt.tight_layout()
#
# script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}_nl.png"
# plt.savefig(filename, dpi=150)  # Save image with high resolution
# plt.show()