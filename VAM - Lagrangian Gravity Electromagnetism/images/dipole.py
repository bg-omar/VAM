# Re-import required libraries after kernel reset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}_1.png"


# Step 1: Compute magnetic dipole field for comparison (quasi-static approx)
# Step 2: Compute vorticity ω = ∇ × v
# Step 3: Compute helicity density h = v ⋅ ω

from scipy.ndimage import gaussian_filter

# Set up parameters for a circular vortex loop
R = 1.0  # major radius of the vortex ring
a = 0.1  # core radius (for smoothing)
n_points = 500

# Parametrize the circular vortex ring
theta = np.linspace(0, 2*np.pi, n_points)
ring_x = R * np.cos(theta)
ring_y = R * np.sin(theta)
ring_z = np.zeros_like(theta)

# Define evaluation grid for Biot-Savart (in x-z plane, y=0)
eval_x, eval_z = np.meshgrid(np.linspace(-4, 4, 50), np.linspace(-4, 4, 50))
eval_y = np.zeros_like(eval_x)

# Biot–Savart law: compute velocity induced by vortex filament
def biot_savart_loop(eval_points, ring_x, ring_y, ring_z, Gamma=1.0):
    dtheta = 2*np.pi / len(ring_x)
    v_x = np.zeros_like(eval_points[:, 0])
    v_y = np.zeros_like(eval_points[:, 0])
    v_z = np.zeros_like(eval_points[:, 0])

    for i in range(len(ring_x)):
        # Segment of vortex ring
        x0, y0, z0 = ring_x[i], ring_y[i], ring_z[i]
        x1, y1, z1 = ring_x[(i+1)%n_points], ring_y[(i+1)%n_points], ring_z[(i+1)%n_points]
        dl = np.array([x1 - x0, y1 - y0, z1 - z0])
        segment_center = np.array([0.5*(x0 + x1), 0.5*(y0 + y1), 0.5*(z0 + z1)])

        # Vector from segment to eval point
        r = eval_points - segment_center
        r_mag = np.linalg.norm(r, axis=1)
        r_cross_dl = np.cross(dl, r)
        denom = (r_mag**3 + a**3)  # Add core smoothing

        # Biot–Savart contribution
        v = Gamma / (4*np.pi) * r_cross_dl.T / denom
        v_x += v[0]
        v_y += v[1]
        v_z += v[2]

    return np.stack([v_x, v_y, v_z], axis=1)

# Flatten grid and compute field
eval_points = np.stack([eval_x.ravel(), eval_y.ravel(), eval_z.ravel()], axis=1)
velocity_field = biot_savart_loop(eval_points, ring_x, ring_y, ring_z)

# Reshape for plotting
U = velocity_field[:, 0].reshape(eval_x.shape)
W = velocity_field[:, 2].reshape(eval_z.shape)

# Plot velocity field in x-z plane
plt.figure(figsize=(8, 6))
plt.streamplot(eval_x, eval_z, U, W, density=1.2, linewidth=1)
plt.plot(ring_x, ring_z, 'r-', label='Vortex Ring')
plt.xlabel('x')
plt.ylabel('z')
plt.title('Biot–Savart-Induced Velocity Field from Vortex Ring (x–z plane)')
plt.axis('equal')
plt.grid(True)
plt.legend()

plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()

# Constants for comparison
mu0 = 4 * np.pi * 1e-7  # Vacuum permeability (just for analogy)
m_dipole = np.array([0, 1, 0])  # Magnetic dipole along y (out of x-z plane)

# Create larger evaluation grid for visible dipole field
eval_x_large, eval_z_large = np.meshgrid(np.linspace(-4, 4, 80), np.linspace(-4, 4, 80))

# Reuse the same function — no need to redefine
def magnetic_dipole_field(x, z, m):
    r_vec = np.stack([x, np.zeros_like(x), z], axis=-1)
    r_mag = np.linalg.norm(r_vec, axis=-1, keepdims=True)
    dot = np.sum(m * r_vec, axis=-1, keepdims=True)
    field = (3 * r_vec * dot / (r_mag**5)) - (m / (r_mag**3))
    return field[..., 0], field[..., 2]  # return x and z components


# Calculate magnetic field components
Bx, Bz = magnetic_dipole_field(eval_x, eval_z, m_dipole)

# Step 2: Compute vorticity ω = ∇ × v
dvz_dx, dvz_dz = np.gradient(W, eval_x[0], eval_z[:, 0])
dvx_dx, dvx_dz = np.gradient(U, eval_x[0], eval_z[:, 0])
vorticity_y = dvz_dx - dvx_dz  # Only y-component relevant in x-z plane

# Step 3: Compute helicity density h = v ⋅ ω (in x-z plane, so scalar here)
helicity_density = U * 0 + W * 0 + vorticity_y * 0  # since v in x-z, ω in y → use U * ω_y as proxy
helicity_density = U * vorticity_y  # local alignment of velocity and vorticity

# Smooth for visualization
vorticity_y_smooth = gaussian_filter(vorticity_y, sigma=1)
helicity_density_smooth = gaussian_filter(helicity_density, sigma=1)

# Redefine a stronger dipole moment vector aligned within the x–z plane
m_dipole_visible = np.array([0, 0, 1])  # Dipole aligned along z-axis (into the plane)

# Recompute magnetic dipole field with new orientation
Bx_visible, Bz_visible = magnetic_dipole_field(eval_x_large, eval_z_large, m_dipole_visible)

# Normalize vector field for visualization
magnitude_visible = np.sqrt(Bx_visible**2 + Bz_visible**2)
Bx_norm = Bx_visible / (magnitude_visible + 1e-12)
Bz_norm = Bz_visible / (magnitude_visible + 1e-12)

# Plot normalized dipole field with visible structure
plt.figure(figsize=(8, 6))
plt.streamplot(eval_x_large, eval_z_large, Bx_norm, Bz_norm, color='blue', linewidth=1, density=1.5)
plt.title("Normalized Magnetic Dipole Field (Dipole Aligned Along z-axis)")
plt.xlabel('x')
plt.ylabel('z')
plt.xlim(-4, 4)
plt.ylim(-4, 4)
plt.axis('equal')
plt.grid(True)
plt.tight_layout()

filename = f"{script_name}_2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution


# Plot vorticity field (ω_y)
plt.figure(figsize=(8, 6))
plt.contourf(eval_x, eval_z, vorticity_y_smooth, levels=30, cmap='RdBu_r')
plt.colorbar(label=r'$\omega_y$')
plt.title("Vorticity Field $\\omega_y = (\\nabla \\times \\vec{v})_y$")
plt.xlabel('x')
plt.ylabel('z')
plt.axis('equal')
plt.grid(True)
plt.tight_layout()

filename = f"{script_name}_3.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution


# Plot helicity density h = v ⋅ ω
plt.figure(figsize=(8, 6))
plt.contourf(eval_x, eval_z, helicity_density_smooth, levels=30, cmap='plasma')
plt.colorbar(label=r'Helicity Density $h = \vec{v} \cdot \vec{\omega}$')
plt.title("Helicity Density Field in x–z Plane")
plt.xlabel('x')
plt.ylabel('z')
plt.axis('equal')
plt.grid(True)
plt.tight_layout()

filename = f"{script_name}_4.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

plt.show()
