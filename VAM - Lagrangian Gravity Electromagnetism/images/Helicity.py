import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ace_tools_open as tools

# Correct the DataFrame structure
df = pd.DataFrame({
    "Quantity": ["Circulation Γ", "Swirl Energy $U_{vortex}$", "Helicity H"],
    "Value": ["−6.80 × 10⁻¹⁸", "3.61 × 10⁻⁷", "2.84 × 10⁻¹⁵"],
    "Units": ["m²/s", "J (2D slice)", "m⁴/s² (2D slice)"]
})

tools.display_dataframe_to_user(name="Photon Ring Vortex Quantities", dataframe=df)

# Set up the grid in the x-z plane
x = np.linspace(-2, 2, 300)
z = np.linspace(-2, 2, 300)
X, Z = np.meshgrid(x, z)

# Parameters for the vortex ring
R = 1.0       # major radius of the torus (m)
r0 = 0.3      # minor (core) radius of the torus (m)
H_total = 2.84e-15  # total helicity (arbitrary units for visualization)

# Compute distance from each point in the x-z plane to the toroidal core
distance_to_ring = np.sqrt((np.sqrt(X**2 + Z**2) - R)**2 + Z**2)

# Approximate helicity density field (Gaussian decay from ring center)
h = H_total * np.exp(-((distance_to_ring / r0) ** 2))

# Plot the helicity density field
plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Z, h, levels=100, cmap='inferno')
plt.colorbar(contour, label=r'Helicity density $h = \vec{v} \cdot \vec{\omega}$')
plt.title('Helicity Density Field in the $x$–$z$ Plane')
plt.xlabel('$x$ (m)')
plt.ylabel('$z$ (m)')
plt.axis('equal')
plt.grid(False)

# Save the figure
plt.savefig("helicity_density_integrated.png", dpi=300, bbox_inches='tight')



# Create an image visualizing the integrated helicity scalar over a vortex ring configuration

# Redefine h to be normalized and compute total helicity scalar for annotation
h_norm = h / np.max(h) * H_total
H_integrated = np.sum(h_norm) * (x[1] - x[0]) * (z[1] - z[0])  # approximate integral over x-z

# Plot the scalar helicity integration visualization
plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Z, h_norm, levels=100, cmap='plasma')
plt.colorbar(contour, label=r'Helicity Density $h = \vec{v} \cdot \vec{\omega}$')
plt.title(f'Integrated Helicity Field: $H \\approx {H_integrated:.2e}$')
plt.xlabel('$x$ (m)')
plt.ylabel('$z$ (m)')
plt.axis('equal')
plt.grid(False)

# Save the figure
output_path2 = "helicity_ring_integration1.png"
plt.savefig(output_path2, dpi=300, bbox_inches='tight')


import numpy as np
import matplotlib.pyplot as plt

# Define a grid in cylindrical coordinates
R, Z = np.meshgrid(np.linspace(0, 4, 400), np.linspace(-2, 2, 400))
r_c = 1.40897017e-15  # vortex core radius (used for structure, but rescaled for plotting)

# Define a simplified helicity density profile for a toroidal vortex
# Peak helicity near ring of radius R0 in the xz-plane
R0 = 2.0
delta = 0.3

# Toroidal profile: centered at (R0, z=0), with exponential fall-off
h = np.exp(-((R - R0)**2 + Z**2) / delta**2) * np.sign(R - R0)

# Create a colormap plot
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.contourf(R, Z, h, levels=100, cmap='seismic')
cbar = plt.colorbar(im, ax=ax, label=r'Helicity density $h = \vec{v} \cdot \vec{\omega}$')

ax.set_xlabel('Radial coordinate $R$')
ax.set_ylabel('Axial coordinate $Z$')
ax.set_title('Helicity Density Field of Toroidal Vortex (Photon Ring Analogy)')
ax.set_aspect('equal')

# Save figure
output_path = "helicity_ring_integration.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')



plt.show()


















