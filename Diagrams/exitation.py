# Re-import necessary libraries after execution state reset
import numpy as np
import matplotlib.pyplot as plt

# Define parameters
theta = np.linspace(0, 2*np.pi, 500)  # Angular position
r = np.linspace(0.2, 2, 500)  # Radial distance
R, Theta = np.meshgrid(2*r, theta)  # Meshgrid for 3D plotting

# Define vortex field function
vortex_intensity = np.sin(Theta) * np.exp(-R)

# Convert to Cartesian coordinates for plotting
X = R * np.cos(Theta)
Y = R * np.sin(Theta)

# Plot vortex excitation structure
plt.figure(figsize=(8, 6))
plt.contourf(X, Y, vortex_intensity, cmap='viridis', levels=30)
plt.colorbar(label="Vortex Intensity")
plt.xlabel("X-axis (Vortex Radius)")
plt.ylabel("Y-axis (Vortex Circulation)")
plt.title("Structured Vortex Excitations in Magnetic Field Formation")
plt.grid(True)
plt.show()