import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from numpy.fft import ifftn
from scipy.fft import fftn

# Define radial and angular grid
r = np.linspace(0, 5, 200)  # Scaled radial distance in units of a_0
theta = np.linspace(0, 2*np.pi, 200)  # Angular coordinate

# Create meshgrid for polar plot
R, Theta = np.meshgrid(r, theta)

# Define wavefunctions (interpreted as vorticity amplitude in VAM)
def psi_1s(r):
    """Ground-state hydrogenic wavefunction (1s orbital)"""
    return np.exp(-r)

def psi_2p(r, theta):
    """First excited state (2p orbital) with angular dependence"""
    return r * np.exp(-r/2) * np.cos(theta)

def psi_3d(r, theta):
    """Second excited state (3d orbital) with angular dependence"""
    return (r**2) * np.exp(-r/3) * np.sin(2*theta)

# Compute values
Z_1s = psi_1s(R)
Z_2p = psi_2p(R, Theta)
Z_3d = psi_3d(R, Theta)

# Define nodal structures for overlay
nodes_1s = np.where(np.abs(Z_1s) < 0.05, 1, 0)
nodes_2p = np.where(np.abs(Z_2p) < 0.05, 1, 0)
nodes_3d = np.where(np.abs(Z_3d) < 0.05, 1, 0)

# Create figure with multiple subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 6), subplot_kw={'projection': 'polar'})

# Normalize color scaling
norm = Normalize(vmin=-1, vmax=1)

# Plot the electron orbitals with nodal structures
p1 = axes[0].contourf(Theta, R, Z_1s, levels=50, cmap='plasma', norm=norm)
axes[0].contour(Theta, R, nodes_1s, levels=1, colors='white', linewidths=1.5)  # Overlay nodal lines
axes[0].set_title('1s Orbital (Spherical Vortex)')

p2 = axes[1].contourf(Theta, R, Z_2p, levels=50, cmap='plasma', norm=norm)
axes[1].contour(Theta, R, nodes_2p, levels=1, colors='white', linewidths=1.5)  # Overlay nodal lines
axes[1].set_title('2p Orbital (Toroidal Vortex)')

p3 = axes[2].contourf(Theta, R, Z_3d, levels=50, cmap='plasma', norm=norm)
axes[2].contour(Theta, R, nodes_3d, levels=1, colors='white', linewidths=1.5)  # Overlay nodal lines
axes[2].set_title('3d Orbital (Higher Vortex Mode)')

# Display figure
plt.tight_layout()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()


# Define grid and initial conditions
N = 64  # Grid size
L = 10.0  # Physical size of the domain
dx = L / N  # Grid spacing

# Define vorticity field (omega) as a Gaussian distribution
x = np.linspace(-L/2, L/2, N, endpoint=False)
y = np.linspace(-L/2, L/2, N, endpoint=False)
X, Y = np.meshgrid(x, y)

# Initial vorticity field as a localized vortex
omega = np.exp(-((X**2 + Y**2) / 2.0))

# Compute velocity field using the Biot-Savart relation in Fourier space
kx = 2 * np.pi * np.fft.fftfreq(N, d=dx)
ky = 2 * np.pi * np.fft.fftfreq(N, d=dx)
KX, KY = np.meshgrid(kx, ky)

# Fourier transform of vorticity
omega_hat = fftn(omega)

# Compute velocity components in Fourier space
psi_hat = -omega_hat / (KX**2 + KY**2 + 1e-6)  # Stream function (small number added for stability)
ux_hat = 1j * KY * psi_hat  # Velocity component in x direction
uy_hat = -1j * KX * psi_hat  # Velocity component in y direction

# Transform back to real space
ux = np.real(ifftn(ux_hat))
uy = np.real(ifftn(uy_hat))

# Plot results
fig, ax = plt.subplots(figsize=(6, 6))
ax.streamplot(x, y, ux, uy, color='b', density=2)
ax.set_title("Vortex-Induced Velocity Field in VAM")
ax.set_xlabel("X")
ax.set_ylabel("Y")
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()