import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D

# Constants
R = 1.0  # Radius of the domain
U = 1.0  # Characteristic velocity
alpha = 3.8317  # First root of J1(x) = 0

# Define the polar grid
n_r = 50  # Number of points in radial direction
n_theta = 100  # Number of points in angular direction

r = np.linspace(0, R, n_r)
theta = np.linspace(0, 2 * np.pi, n_theta)
R_mesh, Theta_mesh = np.meshgrid(r, theta, indexing='xy')  # Use 'xy' for proper shape alignment

# Convert to Cartesian coordinates
X = R_mesh * np.cos(Theta_mesh)
Y = R_mesh * np.sin(Theta_mesh)

# Compute stream function
Psi = U * R * jv(1, alpha * R_mesh / R) * np.sin(Theta_mesh)

# Compute velocity field in polar coordinates
Ur = (U * R * alpha / R) * jv(1, alpha * R_mesh / R) * np.cos(Theta_mesh)
Utheta = -U * alpha * jv(0, alpha * R_mesh / R) * np.sin(Theta_mesh)

# Convert velocity to Cartesian components
U_x = Ur * np.cos(Theta_mesh) - Utheta * np.sin(Theta_mesh)
U_y = Ur * np.sin(Theta_mesh) + Utheta * np.cos(Theta_mesh)

# Create a Cartesian grid for streamplot
x_lin = np.linspace(-R, R, 150)
y_lin = np.linspace(-R, R, 150)

X_grid, Y_grid = np.meshgrid(x_lin, y_lin)

# Interpolate the velocity field onto the Cartesian grid
U_x_interp = griddata((X.flatten(), Y.flatten()), U_x.flatten(), (X_grid, Y_grid), method='cubic')
U_y_interp = griddata((X.flatten(), Y.flatten()), U_y.flatten(), (X_grid, Y_grid), method='cubic')
Psi_interp = griddata((X.flatten(), Y.flatten()), Psi.flatten(), (X_grid, Y_grid), method='cubic')

# Mask out regions outside the circle
mask = X_grid**2 + Y_grid**2 > R**2
U_x_interp[mask] = np.nan
U_y_interp[mask] = np.nan
Psi_interp[mask] = np.nan

# Plot the 3D streamline plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X_grid, Y_grid, Psi_interp, cmap='viridis', edgecolor='k', alpha=0.7)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("Stream Function Ψ")
ax.set_title("3D Lamb-Chaplygin Dipole Streamlines")




# Define Cartesian grid for streamplot
x_lin = np.linspace(-R, R, 50)
y_lin = np.linspace(-R, R, 50)
X_grid, Y_grid = np.meshgrid(x_lin, y_lin)

# Interpolate velocity field onto the Cartesian grid
U_x_interp = griddata((X.flatten(), Y.flatten()), U_x.flatten(), (X_grid, Y_grid), method='linear')
U_y_interp = griddata((X.flatten(), Y.flatten()), U_y.flatten(), (X_grid, Y_grid), method='linear')
U_x_interp[np.sqrt(X_grid**2 + Y_grid**2) < (0.05*R)**2] = 0
U_y_interp[X_grid**2 + Y_grid**2 < (0.05*R)**2] = 0
Psi_interp = griddata((X.flatten(), Y.flatten()), Psi.flatten(), (X_grid, Y_grid), method='linear')
Psi_interp[X_grid**2 + Y_grid**2 < (0.05*R)**2] = 0

# Mask values outside the circular domain
mask = X_grid**2 + Y_grid**2 > R**2
U_x_interp[mask] = np.nan
U_y_interp[mask] = np.nan
Psi_interp[mask] = np.nan

# Create figure
fig, ax = plt.subplots(figsize=(7, 7))

# Contour plot of the stream function
contour = ax.contourf(X_grid, Y_grid, Psi_interp, levels=30, cmap='RdBu', alpha=0.75)

# Streamlines of the velocity field
ax.streamplot(X_grid, Y_grid, U_x_interp, U_y_interp, color='k', linewidth=0.8, density=1.2)

# Dashed circle to mark the boundary
circle = plt.Circle((0, 0), R, color='k', linestyle='dashed', fill=False, linewidth=2)
ax.add_patch(circle)

# Axis labels and title
ax.set_xlabel(r'$x R^{-1}$')
ax.set_ylabel(r'$y R^{-1}$')
ax.set_title("Lamb-Chaplygin Dipole Flow Structure")

# Set limits and aspect ratio
ax.set_xlim(-1.5 * R, 1.5 * R)
ax.set_ylim(-1.5 * R, 1.5 * R)
ax.set_aspect('equal')

# Add color bar
cbar = plt.colorbar(contour)
cbar.set_label(r'Stream Function $\Psi$')



from scipy.interpolate import RectBivariateSpline

# Define fine Cartesian grid for improved interpolation
x_lin = np.linspace(-R, R, 250)
y_lin = np.linspace(-R, R, 250)
X_grid, Y_grid = np.meshgrid(x_lin, y_lin)

# Create interpolation functions using RectBivariateSpline (better structured interpolation)
interp_Psi = RectBivariateSpline(r, theta, Psi.T, kx=3, ky=3)
interp_Ux = RectBivariateSpline(r, theta, U_x.T, kx=3, ky=3)
interp_Uy = RectBivariateSpline(r, theta, U_y.T, kx=3, ky=3)

# Convert Cartesian coordinates to polar for evaluation
R_eval = np.sqrt(X_grid**2 + Y_grid**2)
Theta_eval = np.arctan2(Y_grid, X_grid)

# Evaluate interpolated values
Psi_interp = interp_Psi.ev(R_eval, Theta_eval)
U_x_interp = interp_Ux.ev(R_eval, Theta_eval)
U_y_interp = interp_Uy.ev(R_eval, Theta_eval)

# Set the stream function at the origin to zero explicitly
Psi_interp[R_eval < (0.05 * R)] = 0

# Mask values outside the circular domain
mask = R_eval > R
Psi_interp[mask] = np.nan
U_x_interp[mask] = np.nan
U_y_interp[mask] = np.nan

# Create figure
fig, ax = plt.subplots(figsize=(7, 7))

# Contour plot of the stream function
contour = ax.contourf(X_grid, Y_grid, Psi_interp, levels=30, cmap='RdBu', alpha=0.75)

# Streamlines of the velocity field
ax.streamplot(X_grid, Y_grid, U_x_interp, U_y_interp, color='k', linewidth=0.8, density=1.2)

# Dashed circle to mark the boundary
circle = plt.Circle((0, 0), R, color='k', linestyle='dashed', fill=False, linewidth=2)
ax.add_patch(circle)

# Axis labels and title
ax.set_xlabel(r'$x R^{-1}$')
ax.set_ylabel(r'$y R^{-1}$')
ax.set_title("Lamb-Chaplygin Dipole Flow Structure (Refined Interpolation)")

# Set limits and aspect ratio
ax.set_xlim(-1.5 * R, 1.5 * R)
ax.set_ylim(-1.5 * R, 1.5 * R)
ax.set_aspect('equal')

# Add color bar
cbar = plt.colorbar(contour)
cbar.set_label(r'Stream Function $\Psi$')

# Show the plot
plt.show()