import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to plot a simple vortex in 3D
def plot_vortex_3d(ax):
    theta = np.linspace(0, 2 * np.pi, 100)
    z = np.linspace(-1, 1, 50)
    for zi in z:
        x = np.cos(theta)
        y = np.sin(theta)
        ax.plot(x, y, zi, 'b', alpha=0.5)
    ax.set_title("3D Vortex")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

# Function to plot a vortex line in 3D
def plot_vortex_line_3d(ax):
    z = np.linspace(-1, 1, 100)
    x = np.zeros_like(z)
    y = np.zeros_like(z)
    ax.plot(x, y, z, 'b', linewidth=2)
    ax.set_title("3D Vortex Line")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

# Function to plot a vortex tube in 3D
def plot_vortex_tube_3d(ax):
    theta = np.linspace(0, 2 * np.pi, 100)
    z = np.linspace(-1, 1, 50)
    for zi in z[::10]:
        x = np.cos(theta)
        y = np.sin(theta)
        ax.plot(x, y, zi, 'b', alpha=0.5)
    ax.set_title("3D Vortex Tube")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

# Function to plot a trefoil knot vortex in 3D
def plot_trefoil_knot_3d(ax):
    t = np.linspace(0, 2 * np.pi, 100)
    x = np.sin(t) + 2 * np.sin(2 * t)
    y = np.cos(t) - 2 * np.cos(2 * t)
    z = -np.sin(3 * t)
    ax.plot(x, y, z, 'b', linewidth=2)
    ax.set_title("3D Trefoil Knot Vortex")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

# Create a figure with subplots for each 3D plot
fig = plt.figure(figsize=(15, 10))

ax1 = fig.add_subplot(221, projection='3d')
plot_vortex_3d(ax1)

ax2 = fig.add_subplot(222, projection='3d')
plot_vortex_line_3d(ax2)

ax3 = fig.add_subplot(223, projection='3d')
plot_vortex_tube_3d(ax3)

ax4 = fig.add_subplot(224, projection='3d')
plot_trefoil_knot_3d(ax4)

plt.tight_layout()
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()