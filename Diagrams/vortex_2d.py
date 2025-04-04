import matplotlib.pyplot as plt
import numpy as np

# Function to plot a simple vortex
def plot_vortex(ax):
    theta = np.linspace(0, 2 * np.pi, 100)
    r = np.linspace(0.1, 1, 10)
    for radius in r:
        ax.plot(radius * np.cos(theta), radius * np.sin(theta), 'b', alpha=0.5)
    ax.set_title("Vortex")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

# Function to plot a vortex line
def plot_vortex_line(ax):
    x = np.linspace(-1, 1, 100)
    y = np.zeros_like(x)
    ax.plot(x, y, 'b', linewidth=2)
    ax.set_title("Vortex Line")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

# Function to plot a vortex tube
def plot_vortex_tube(ax):
    theta = np.linspace(0, 2*np.pi, 100)
    z = np.linspace(-1, 1, 50)
    for height in z[::10]:
        ax.plot(np.cos(theta), np.sin(theta) + height, 'b', alpha=0.5)
    ax.set_title("Vortex Tube")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

# Function to plot rotational vortex core
def plot_rotational_vortex_core(ax):
    theta = np.linspace(0, 2 * np.pi, 100)
    r = np.linspace(0.1, 0.5, 5)
    for radius in r:
        ax.plot(radius * np.cos(theta), radius * np.sin(theta), 'r', alpha=0.5)
    ax.plot(0.5 * np.cos(theta), 0.5 * np.sin(theta), 'b', linewidth=2)
    ax.set_title("Rotational Vortex Core")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

# Function to plot irrotational vortex
def plot_irrotational_vortex(ax):
    theta = np.linspace(0, 2 * np.pi, 100)
    r = np.linspace(0.5, 1, 5)
    for radius in r:
        ax.plot(radius * np.cos(theta), radius * np.sin(theta), 'b', alpha=0.5)
    ax.set_title("Irrotational Vortex")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

# Function to plot a trefoil knot vortex (approximation)
def plot_trefoil_knot(ax):
    t = np.linspace(0, 2 * np.pi, 100)
    x = np.sin(t) + 2 * np.sin(2 * t)
    y = np.cos(t) - 2 * np.cos(2 * t)
    ax.plot(x, y, 'b', linewidth=2)
    ax.set_title("Trefoil Knot Vortex")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

# Create figures for each concept
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

plot_vortex(axes[0, 0])
plot_vortex_line(axes[0, 1])
plot_vortex_tube(axes[0, 2])
plot_rotational_vortex_core(axes[1, 0])
plot_irrotational_vortex(axes[1, 1])
plot_trefoil_knot(axes[1, 2])

plt.tight_layout()
plt.show()