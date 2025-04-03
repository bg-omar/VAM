# Re-import necessary libraries since execution state was reset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import genlaguerre
from scipy.constants import physical_constants

# Define grid for 3D plot
theta = np.linspace(0, 2 * np.pi, 100)  # Angular component
r = np.linspace(0, 3, 100)  # Radial component (normalized units)
R, Theta = np.meshgrid(r, theta)  # Create meshgrid

# Define Rc and a0 in normalized units
Rc = 0.2  # Coulomb barrier radius (arbitrary scale)
a0 = 1.0  # Bohr radius (arbitrary scale)

# Define the vortex swirl profile
v_theta = (1 - np.exp(-(R - Rc) / a0)) * (R > Rc)
v_theta[R < Rc] = 0  # Suppress swirl inside Rc

# Convert to Cartesian coordinates for plotting
X = R * np.cos(Theta)
Y = R * np.sin(Theta)
Z = v_theta  # Swirl amplitude

# Create 3D plot with a highlighted blue line at the nodal region
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Surface plot
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.5)

# Define the nodal region (peak swirl amplitude, around r ≈ a0)
node_r = np.full_like(theta, a0)  # Constant radius at a0
node_x = node_r * np.cos(theta)
node_y = node_r * np.sin(theta)
node_z = (1 - np.exp(-(a0 - Rc) / a0)) * np.ones_like(theta)  # Corresponding amplitude

# Plot the nodal ring in blue
ax.plot(node_x, node_y, node_z, color='blue', linewidth=3, label="1s Orbital Node")


# Define a second vortex mode for the 2s orbital
v_theta_2s = (1 - np.exp(-(R - Rc) / a0)) * (1 - 2 * np.exp(-(R - 2*a0) / a0)) * (R > Rc)
v_theta_2s[R < Rc] = 0  # Suppress swirl inside Rc

# Convert to Cartesian coordinates for plotting
Z_2s = v_theta_2s  # Swirl amplitude for 2s orbital

# Create 3D plot with both 1s and 2s orbitals and marked nodes
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Surface plot for 1s orbital (transparent)
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.3, label="1s Orbital")

# Surface plot for 2s orbital (transparent)
ax.plot_surface(X, Y, Z_2s, cmap='plasma', edgecolor='none', alpha=0.3, label="2s Orbital")

# Define the first nodal region (peak swirl amplitude for 1s orbital)
node_x_1s = a0 * np.cos(theta)
node_y_1s = a0 * np.sin(theta)
node_z_1s = (1 - np.exp(-(a0 - Rc) / a0)) * np.ones_like(theta)

# Define the second nodal region (for 2s orbital at ~2a0)
node_x_2s = 2 * a0 * np.cos(theta)
node_y_2s = 2 * a0 * np.sin(theta)
node_z_2s = (1 - np.exp(-(2*a0 - Rc) / a0)) * np.ones_like(theta)

# Plot the 1s nodal ring in blue
ax.plot(node_x_1s, node_y_1s, node_z_1s, color='blue', linewidth=3, label="1s Orbital Node")

# Plot the 2s nodal ring in red
ax.plot(node_x_2s, node_y_2s, node_z_2s, color='red', linewidth=3, label="2s Orbital Node")

# Define additional higher-order orbitals: 3s, 4s
v_theta_3s = (1 - np.exp(-(R - Rc) / a0)) * (1 - 2 * np.exp(-(R - 2*a0) / a0)) * (1 - 3 * np.exp(-(R - 3*a0) / a0)) * (R > Rc)
v_theta_3s[R < Rc] = 0  # Suppress swirl inside Rc

v_theta_4s = (1 - np.exp(-(R - Rc) / a0)) * (1 - 2 * np.exp(-(R - 2*a0) / a0)) * (1 - 3 * np.exp(-(R - 3*a0) / a0)) * (1 - 4 * np.exp(-(R - 4*a0) / a0)) * (R > Rc)
v_theta_4s[R < Rc] = 0  # Suppress swirl inside Rc

# Convert to Cartesian coordinates for plotting
Z_3s = v_theta_3s  # Swirl amplitude for 3s orbital
Z_4s = v_theta_4s  # Swirl amplitude for 4s orbital

# Create figure
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Surface plots for each orbital (transparent for visualization)
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.3)  # 1s
ax.plot_surface(X, Y, Z_2s, cmap='plasma', edgecolor='none', alpha=0.3)  # 2s
ax.plot_surface(X, Y, Z_3s, cmap='inferno', edgecolor='none', alpha=0.3)  # 3s
ax.plot_surface(X, Y, Z_4s, cmap='magma', edgecolor='none', alpha=0.3)  # 4s

# Define nodal regions for higher orbitals (radii: a0, 2a0, 3a0, 4a0)
node_x_3s = 3 * a0 * np.cos(theta)
node_y_3s = 3 * a0 * np.sin(theta)
node_z_3s = (1 - np.exp(-(3*a0 - Rc) / a0)) * np.ones_like(theta)

node_x_4s = 4 * a0 * np.cos(theta)
node_y_4s = 4 * a0 * np.sin(theta)
node_z_4s = (1 - np.exp(-(4*a0 - Rc) / a0)) * np.ones_like(theta)

# Plot the nodal rings
ax.plot(node_x_1s, node_y_1s, node_z_1s, color='blue', linewidth=3, label="1s Orbital Node")
ax.plot(node_x_2s, node_y_2s, node_z_2s, color='red', linewidth=3, label="2s Orbital Node")
ax.plot(node_x_3s, node_y_3s, node_z_3s, color='green', linewidth=3, label="3s Orbital Node")
ax.plot(node_x_4s, node_y_4s, node_z_4s, color='purple', linewidth=3, label="4s Orbital Node")

# Labels and title
ax.set_xlabel(r'$x$ (normalized units)')
ax.set_ylabel(r'$y$ (normalized units)')
ax.set_zlabel(r'Vortex Swirl Amplitude')
ax.set_title(r'Electron Vortex Swirl (VAM Interpretation of s Orbitals)')

# Manually create legend entries
legend_elements = [
    plt.Line2D([0], [0], color='blue', lw=3, label="1s Orbital Node"),
    plt.Line2D([0], [0], color='red', lw=3, label="2s Orbital Node"),
    plt.Line2D([0], [0], color='green', lw=3, label="3s Orbital Node"),
    plt.Line2D([0], [0], color='purple', lw=3, label="4s Orbital Node")
]
ax.legend(handles=legend_elements)


# Define a function to normalize amplitudes relative to 1s maximum
def normalize(v_theta):
    return v_theta / np.max(v_theta)

# Normalize vortex swirl amplitudes
Z_norm_1s = normalize(Z)
Z_norm_2s = normalize(Z_2s)
Z_norm_3s = normalize(Z_3s)
Z_norm_4s = normalize(Z_4s)

# Define corresponding Schrödinger wavefunction amplitudes (exponential decay-based)
Z_sch_1s = np.exp(-R / a0) * (R > Rc)  # 1s wavefunction
Z_sch_2s = (1 - R / (2*a0)) * np.exp(-R / (2*a0)) * (R > Rc)  # 2s wavefunction
Z_sch_3s = (1 - 2 * R / (3*a0)) * np.exp(-R / (3*a0)) * (R > Rc)  # 3s wavefunction
Z_sch_4s = (1 - 3 * R / (4*a0)) * np.exp(-R / (4*a0)) * (R > Rc)  # 4s wavefunction

# Normalize Schrödinger wavefunctions
Z_sch_1s = normalize(Z_sch_1s)
Z_sch_2s = normalize(Z_sch_2s)
Z_sch_3s = normalize(Z_sch_3s)
Z_sch_4s = normalize(Z_sch_4s)

# Create figure with two subplots: VAM (left) vs Schrödinger (right)
fig = plt.figure(figsize=(14, 6))

# Left plot: VAM Interpretation
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(X, Y, Z_norm_1s, cmap='viridis', edgecolor='none', alpha=0.3)
ax1.plot_surface(X, Y, Z_norm_2s, cmap='plasma', edgecolor='none', alpha=0.3)
ax1.plot_surface(X, Y, Z_norm_3s, cmap='inferno', edgecolor='none', alpha=0.3)
ax1.plot_surface(X, Y, Z_norm_4s, cmap='magma', edgecolor='none', alpha=0.3)

# Plot nodal circles in VAM
ax1.plot(node_x_1s, node_y_1s, node_z_1s, color='blue', linewidth=3)
ax1.plot(node_x_2s, node_y_2s, node_z_2s, color='red', linewidth=3)
ax1.plot(node_x_3s, node_y_3s, node_z_3s, color='green', linewidth=3)
ax1.plot(node_x_4s, node_y_4s, node_z_4s, color='purple', linewidth=3)

# Labels for VAM
ax1.set_xlabel(r'$x$ (normalized)')
ax1.set_ylabel(r'$y$ (normalized)')
ax1.set_zlabel(r'Vortex Swirl Amplitude')
ax1.set_title(r'VAM Interpretation of s Orbitals')

# Right plot: Schrödinger QM Interpretation
ax2 = fig.add_subplot(122, projection='3d')
ax2.plot_surface(X, Y, Z_sch_1s, cmap='viridis', edgecolor='none', alpha=0.3)
ax2.plot_surface(X, Y, Z_sch_2s, cmap='plasma', edgecolor='none', alpha=0.3)
ax2.plot_surface(X, Y, Z_sch_3s, cmap='inferno', edgecolor='none', alpha=0.3)
ax2.plot_surface(X, Y, Z_sch_4s, cmap='magma', edgecolor='none', alpha=0.3)

# Plot nodal circles in QM
ax2.plot(node_x_1s, node_y_1s, node_z_1s, color='blue', linewidth=3)
ax2.plot(node_x_2s, node_y_2s, node_z_2s, color='red', linewidth=3)
ax2.plot(node_x_3s, node_y_3s, node_z_3s, color='green', linewidth=3)
ax2.plot(node_x_4s, node_y_4s, node_z_4s, color='purple', linewidth=3)

# Labels for Schrödinger
ax2.set_xlabel(r'$x$ (normalized)')
ax2.set_ylabel(r'$y$ (normalized)')
ax2.set_zlabel(r'Probability Amplitude')
ax2.set_title(r'Schrödinger QM Interpretation of s Orbitals')

# # Show plot
# plt.show()

# Recompute vortex swirl amplitudes without forced symmetry
def vam_vortex_swirl(R, Rc, a0, n):
    """Computes the natural vortex swirl amplitude for the nth s-orbital in VAM."""
    return (1 - n * np.exp(-(R - n * Rc) / (n * a0))) * (R > Rc)

# Compute raw VAM amplitudes for 1s, 2s, 3s, 4s
Z_vam_1s = vam_vortex_swirl(R, Rc, a0, 1)
Z_vam_2s = vam_vortex_swirl(R, Rc, a0, 2)
Z_vam_3s = vam_vortex_swirl(R, Rc, a0, 3)
Z_vam_4s = vam_vortex_swirl(R, Rc, a0, 4)

# Recompute Schrödinger wavefunctions naturally
def schrodinger_wavefunction(R, a0, n):
    """Computes the natural Schrödinger wavefunction for the nth s-orbital."""
    return (1 - (n-1) * R / (n * a0)) * np.exp(-R / (n * a0)) * (R > Rc)

def schrodinger_wavefunction(r, n):
    """Computes the correct radial Schrödinger wavefunction for s-orbitals (ℓ=0)."""
    prefactor = np.sqrt((2 / (n * a0))**3 * np.math.factorial(n - 1) / (2 * n * np.math.factorial(n)))
    rho = 2 * r / (n * a0)  # Scaled radius
    laguerre_poly = genlaguerre(n - 1, 2)(rho)  # Associated Laguerre polynomial
    return prefactor * np.exp(-rho / 2) * laguerre_poly

Z_sch_1s_raw = schrodinger_wavefunction(R, a0, 1)
Z_sch_2s_raw = schrodinger_wavefunction(R, a0, 2)
Z_sch_3s_raw = schrodinger_wavefunction(R, a0, 3)
Z_sch_4s_raw = schrodinger_wavefunction(R, a0, 4)

# Create figure with two subplots: VAM (left) vs Schrödinger (right)
fig = plt.figure(figsize=(14, 6))

# Left plot: VAM Interpretation (Natural Amplitudes)
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(X, Y, Z_vam_1s, cmap='viridis', edgecolor='none', alpha=0.3)
ax1.plot_surface(X, Y, Z_vam_2s, cmap='plasma', edgecolor='none', alpha=0.3)
ax1.plot_surface(X, Y, Z_vam_3s, cmap='inferno', edgecolor='none', alpha=0.3)
ax1.plot_surface(X, Y, Z_vam_4s, cmap='magma', edgecolor='none', alpha=0.3)

# Nodal Rings (should now be naturally placed!)
ax1.plot(node_x_1s, node_y_1s, Z_vam_1s[0, -1] * np.ones_like(theta), color='blue', linewidth=3)
ax1.plot(node_x_2s, node_y_2s, Z_vam_2s[0, -1] * np.ones_like(theta), color='red', linewidth=3)
ax1.plot(node_x_3s, node_y_3s, Z_vam_3s[0, -1] * np.ones_like(theta), color='green', linewidth=3)
ax1.plot(node_x_4s, node_y_4s, Z_vam_4s[0, -1] * np.ones_like(theta), color='purple', linewidth=3)

# Labels for VAM
ax1.set_xlabel(r'$x$ (normalized)')
ax1.set_ylabel(r'$y$ (normalized)')
ax1.set_zlabel(r'Vortex Swirl Amplitude')
ax1.set_title(r'VAM Interpretation of s Orbitals')

# Right plot: Schrödinger QM Interpretation (Natural Amplitudes)
ax2 = fig.add_subplot(122, projection='3d')
ax2.plot_surface(X, Y, Z_sch_1s_raw, cmap='viridis', edgecolor='none', alpha=0.3)
ax2.plot_surface(X, Y, Z_sch_2s_raw, cmap='plasma', edgecolor='none', alpha=0.3)
ax2.plot_surface(X, Y, Z_sch_3s_raw, cmap='inferno', edgecolor='none', alpha=0.3)
ax2.plot_surface(X, Y, Z_sch_4s_raw, cmap='magma', edgecolor='none', alpha=0.3)

# Nodal Rings (Schrödinger Side)
ax2.plot(node_x_1s, node_y_1s, Z_sch_1s_raw[0, -1] * np.ones_like(theta), color='blue', linewidth=3)
ax2.plot(node_x_2s, node_y_2s, Z_sch_2s_raw[0, -1] * np.ones_like(theta), color='red', linewidth=3)
ax2.plot(node_x_3s, node_y_3s, Z_sch_3s_raw[0, -1] * np.ones_like(theta), color='green', linewidth=3)
ax2.plot(node_x_4s, node_y_4s, Z_sch_4s_raw[0, -1] * np.ones_like(theta), color='purple', linewidth=3)

# Labels for Schrödinger
ax2.set_xlabel(r'$x$ (normalized)')
ax2.set_ylabel(r'$y$ (normalized)')
ax2.set_zlabel(r'Probability Amplitude')
ax2.set_title(r'Schrödinger QM Interpretation of s Orbitals')

# Show plot
plt.show()