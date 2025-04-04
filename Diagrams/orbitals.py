import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

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

# Create figure with multiple subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 6), subplot_kw={'projection': 'polar'})

# Normalize color scaling
norm = Normalize(vmin=0, vmax=1)

# Plot the electron orbitals (interpreted as Ætheric vortex swirls)
p1 = axes[0].contourf(Theta, R, Z_1s, levels=50, cmap='plasma', norm=norm)
axes[0].set_title('1s Orbital (Spherical Vortex)')

p2 = axes[1].contourf(Theta, R, Z_2p, levels=50, cmap='plasma', norm=norm)
axes[1].set_title('2p Orbital (Toroidal Vortex)')

p3 = axes[2].contourf(Theta, R, Z_3d, levels=50, cmap='plasma', norm=norm)
axes[2].set_title('3d Orbital (Higher Vortex Mode)')

# Display figure
plt.tight_layout()
plt.show()