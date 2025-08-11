import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
import numpy as np

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Common hydrogen atom layout
proton_radius = 0.2
electron_orbit_radius = 0.6

# Case 1: Moving through æther (SR)
ax = axes[0]
ax.set_title("Hydrogen Atom Moving Through Æther (SR)", fontsize=12)
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')
ax.axis('off')

# Æther flow lines
for y in np.linspace(-1, 1, 10):
    ax.arrow(-1, y, 2, 0, head_width=0.02, head_length=0.05, fc='lightblue', ec='lightblue', alpha=0.6)

# Proton (center)
proton = plt.Circle((0, 0), proton_radius, color='red', alpha=0.8, label='Proton (Quark Knots)')
ax.add_artist(proton)

# Electron orbit
electron_orbit = plt.Circle((0, 0), electron_orbit_radius, color='gray', fill=False, linestyle='--', alpha=0.6)
ax.add_artist(electron_orbit)
electron = plt.Circle((electron_orbit_radius, 0), 0.05, color='blue', alpha=0.8, label='Electron (Unknot/Trefoil)')
ax.add_artist(electron)

# Case 2: Near a massive object (GR)
ax = axes[1]
ax.set_title("Hydrogen Atom in Swirling Æther Near Mass (GR)", fontsize=12)
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')
ax.axis('off')

# Swirl flow lines
theta = np.linspace(0, 2*np.pi, 100)
for r in np.linspace(0.3, 1, 5):
    swirl_x = r * np.cos(theta)
    swirl_y = r * np.sin(theta)
    ax.plot(swirl_x, swirl_y, color='lightblue', alpha=0.6)

# Proton
proton = plt.Circle((0, 0), proton_radius, color='red', alpha=0.8)
ax.add_artist(proton)

# Electron orbit
electron_orbit = plt.Circle((0, 0), electron_orbit_radius, color='gray', fill=False, linestyle='--', alpha=0.6)
ax.add_artist(electron_orbit)
electron = plt.Circle((electron_orbit_radius, 0), 0.05, color='blue', alpha=0.8)
ax.add_artist(electron)

# Add labels
axes[0].legend(loc='upper right', fontsize=8)

plt.show()


# Function to generate a simple trefoil-like knot from Fourier series-like equations
def knot_7_4(num_points=500, scale=1.0):
    t = np.linspace(0, 2*np.pi, num_points)
    # Simplified parametric approximation of a complex knot (stylized, not exact 7_4)
    x = scale * (np.sin(2*t) + 2*np.sin(3*t))
    y = scale * (np.cos(2*t) - 2*np.cos(3*t))
    z = scale * (-np.sin(4*t))
    return x, y, z

# Create figure with two subplots (SR and GR visualization)
fig = plt.figure(figsize=(14, 6))

# SR case - uniform flow
ax1 = fig.add_subplot(121, projection='3d')
x, y, z = knot_7_4()
ax1.plot(x, y, z, color='red', lw=2)
ax1.set_title("7₄ Knot (Down Quark) in Uniform Æther Flow (SR)", fontsize=12)
ax1.quiver(-4, -4, -1, 8, 0, 0, color='lightblue', alpha=0.5, length=8, normalize=False)
ax1.quiver(-4, -2,  1, 8, 0, 0, color='lightblue', alpha=0.5, length=8, normalize=False)
ax1.quiver(-4,  0, -1, 8, 0, 0, color='lightblue', alpha=0.5, length=8, normalize=False)
ax1.quiver(-4,  2,  1, 8, 0, 0, color='lightblue', alpha=0.5, length=8, normalize=False)

# GR case - vortex flow around knot
ax2 = fig.add_subplot(122, projection='3d')
ax2.plot(x, y, z, color='red', lw=2)
ax2.set_title("7₄ Knot (Down Quark) in Vortex Æther Flow (GR)", fontsize=12)

# Create swirl/vortex-like streamlines in XY-plane
theta = np.linspace(0, 2*np.pi, 50)
radii = [2, 3, 4]
for r in radii:
    ax2.plot(r*np.cos(theta), r*np.sin(theta), 0.5*np.sin(2*theta), color='lightblue', alpha=0.5)

# Pressure gradient coloring: closer to knot = darker blue (low 'clock speed')
for r in np.linspace(1, 4, 5):
    ax2.plot(r*np.cos(theta), r*np.sin(theta), 0, color=plt.cm.Blues(1 - r/4), alpha=0.6)

plt.tight_layout()
plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Function to generate a stylized 7_4-like knot curve
def knot_7_4(num_points=500, scale=1.0):
    t = np.linspace(0, 2*np.pi, num_points)
    x = scale * (np.sin(2*t) + 2*np.sin(3*t))
    y = scale * (np.cos(2*t) - 2*np.cos(3*t))
    z = scale * (-np.sin(4*t))
    return x, y, z

# Create figure with two subplots (SR and GR visualization)
fig = plt.figure(figsize=(14, 6))

# SR case - uniform flow
ax1 = fig.add_subplot(121, projection='3d')
x, y, z = knot_7_4()
ax1.plot(x, y, z, color='red', lw=2)
ax1.set_title("7₄ Knot (Down Quark) in Uniform Æther Flow (SR)", fontsize=12)

# Uniform flow arrows
for y_pos in np.linspace(-4, 4, 6):
    for z_pos in np.linspace(-2, 2, 3):
        ax1.quiver(-4, y_pos, z_pos, 8, 0, 0, color='lightblue', alpha=0.5, length=8, normalize=False)

# GR case - vortex flow
ax2 = fig.add_subplot(122, projection='3d')
ax2.plot(x, y, z, color='red', lw=2)
ax2.set_title("7₄ Knot (Down Quark) in Vortex Æther Flow (GR)", fontsize=12)

# Swirl flow lines
theta = np.linspace(0, 2*np.pi, 100)
for r in [2, 3, 4]:
    ax2.plot(r*np.cos(theta), r*np.sin(theta), 0.5*np.sin(2*theta), color='lightblue', alpha=0.5)

# Pressure gradient color rings
for r in np.linspace(1, 4, 5):
    ax2.plot(r*np.cos(theta), r*np.sin(theta), 0, color=plt.cm.Blues(1 - r/4), alpha=0.6)

plt.tight_layout()
plt.show()


# Let's define functions for the 6_4 (up quark) and 3_1 (electron) knots
def knot_6_4(num_points=500, scale=1.0):
    t = np.linspace(0, 2*np.pi, num_points)
    x = scale * (np.sin(3*t) + np.sin(5*t))
    y = scale * (np.cos(3*t) - np.cos(5*t))
    z = scale * (np.sin(4*t))
    return x, y, z

def knot_3_1(num_points=500, scale=1.0):
    t = np.linspace(0, 2*np.pi, num_points)
    x = scale * np.sin(t) + 2*scale * np.sin(2*t)
    y = scale * np.cos(t) - 2*scale * np.cos(2*t)
    z = -scale * np.sin(3*t)
    return x, y, z

# Function to plot SR and GR visualizations for a knot
def plot_knot_with_flows(knot_func, knot_name, color='red'):
    fig = plt.figure(figsize=(14, 6))

    # SR case - uniform flow
    ax1 = fig.add_subplot(121, projection='3d')
    x, y, z = knot_func()
    ax1.plot(x, y, z, color=color, lw=2)
    ax1.set_title(f"{knot_name} in Uniform Æther Flow (SR)", fontsize=12)

    for y_pos in np.linspace(-4, 4, 6):
        for z_pos in np.linspace(-2, 2, 3):
            ax1.quiver(-4, y_pos, z_pos, 8, 0, 0, color='lightblue', alpha=0.5, length=8, normalize=False)

    # GR case - vortex flow
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot(x, y, z, color=color, lw=2)
    ax2.set_title(f"{knot_name} in Vortex Æther Flow (GR)", fontsize=12)

    theta = np.linspace(0, 2*np.pi, 100)
    for r in [2, 3, 4]:
        ax2.plot(r*np.cos(theta), r*np.sin(theta), 0.5*np.sin(2*theta), color='lightblue', alpha=0.5)

    for r in np.linspace(1, 4, 5):
        ax2.plot(r*np.cos(theta), r*np.sin(theta), 0, color=plt.cm.Blues(1 - r/4), alpha=0.6)

    plt.tight_layout()
    plt.show()

# Plot for 6_4 (up quark)
plot_knot_with_flows(knot_6_4, "6₄ Knot (Up Quark)", color='orange')

# Plot for 3_1 (electron)
plot_knot_with_flows(knot_3_1, "3₁ Knot (Electron)", color='blue')
