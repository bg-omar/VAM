


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import dpnp as dnp  # Intel oneAPI SYCL acceleration
import dpctl.tensor as dpt  # oneMKL acceleration
from scipy.ndimage import gaussian_filter
from mpl_toolkits.mplot3d import Axes3D

# Simulation Parameters
dx = 0.01  # Spatial step size (meters)
dt = dx / (2 * 3e8)  # Time step (stability condition)
grid_size = (40, 40, 40)  # High-resolution 3D grid
time_steps = 200  # Total simulation steps

# Physical Constants
mu_0 = 4 * np.pi * 1e-7
epsilon_0 = 8.854e-12
f_res = 10e6  # Resonant frequency (Hz)
omega_res = 2 * np.pi * f_res

# SYCL GPU Memory Allocation using Intel oneMKL (dpctl.tensor)
Ez = dpt.zeros(grid_size, dtype=dpt.float32)
Ex = dpt.zeros(grid_size, dtype=dpt.float32)
Ey = dpt.zeros(grid_size, dtype=dpt.float32)
Bx = dpt.zeros(grid_size, dtype=dpt.float32)
By = dpt.zeros(grid_size, dtype=dpt.float32)
Bz = dpt.zeros(grid_size, dtype=dpt.float32)

# Source Position (Rodin coil center)
source_pos = (grid_size[0] // 2, grid_size[1] // 2, grid_size[2] // 2)

# 3D Grid for Visualization
x_vals = np.linspace(-1, 1, grid_size[0])
y_vals = np.linspace(-1, 1, grid_size[1])
z_vals = np.linspace(-1, 1, grid_size[2])
X, Y, Z = np.meshgrid(x_vals, y_vals, z_vals, indexing='ij')

# Initialize Figure
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# **Reduce Density for Clarity**
subsample_factor = 4  # Less clutter, better readability
X_sub, Y_sub, Z_sub = X[::subsample_factor, ::subsample_factor, ::subsample_factor], \
    Y[::subsample_factor, ::subsample_factor, ::subsample_factor], \
    Z[::subsample_factor, ::subsample_factor, ::subsample_factor]

# **Define Global Quiver Variables to Prevent Unresolved References**
quiver_E = None
quiver_B = None

# **Function to update the animation frame**
def update(frame):
    global quiver_E, quiver_B, Ez, Ex, Ey, Bx, By, Bz

    # **Ensure Stability Before Updating Fields**
    max_float = np.finfo(np.float32).max * 1e-10
    min_float = np.finfo(np.float32).min * 1e-10

    # Update Electric Fields (Faraday's Law)
    Ez[1:, 1:, 1:] -= dpt.clip(
        dt / (epsilon_0 * dx) * ((By[1:, 1:, 1:] - By[:-1, 1:, 1:]) - (Bx[1:, 1:, 1:] - Bx[1:, :-1, 1:])),
        min_float, max_float
    )

    # Apply Oscillating Source in Coil Center
    Ez[source_pos] += dpt.clip(dpt.sin(dpt.asarray(omega_res * frame * dt)) * 1e6, min_float, max_float)

    # Update Magnetic Fields (Ampère-Maxwell Law)
    Bx[:-1, :, :] += dpt.clip(dt / (mu_0 * dx) * (Ez[1:, :, :] - Ez[:-1, :, :]), min_float, max_float)
    By[:, :-1, :] -= dpt.clip(dt / (mu_0 * dx) * (Ez[:, 1:, :] - Ez[:, :-1, :]), min_float, max_float)
    Bz[:, :, :-1] += dpt.clip(dt / (mu_0 * dx) * (Ez[:, :, 1:] - Ez[:, :, :-1]), min_float, max_float)

    # **Fix Indexing: Use Correct Subsampling Instead of `idx, idx, idx`**
    Ex_sub = Ex[::subsample_factor, ::subsample_factor, ::subsample_factor]
    Ey_sub = Ey[::subsample_factor, ::subsample_factor, ::subsample_factor]
    Ez_sub = Ez[::subsample_factor, ::subsample_factor, ::subsample_factor]
    Bx_sub = Bx[::subsample_factor, ::subsample_factor, ::subsample_factor]
    By_sub = By[::subsample_factor, ::subsample_factor, ::subsample_factor]
    Bz_sub = Bz[::subsample_factor, ::subsample_factor, ::subsample_factor]

    # **Ensure Arrays are dpctl.tensor.usm_ndarray Before Applying oneMKL Functions**
    Ex_sub, Ey_sub, Ez_sub = dpt.asarray(Ex_sub), dpt.asarray(Ey_sub), dpt.asarray(Ez_sub)
    Bx_sub, By_sub, Bz_sub = dpt.asarray(Bx_sub), dpt.asarray(By_sub), dpt.asarray(Bz_sub)

    # **Apply Gaussian Smoothing for Coherence**
    Ex_sub, Ey_sub, Ez_sub = gaussian_filter(dpt.to_numpy(Ex_sub), sigma=1), \
        gaussian_filter(dpt.to_numpy(Ey_sub), sigma=1), \
        gaussian_filter(dpt.to_numpy(Ez_sub), sigma=1)

    Bx_sub, By_sub, Bz_sub = gaussian_filter(dpt.to_numpy(Bx_sub), sigma=1), \
        gaussian_filter(dpt.to_numpy(By_sub), sigma=1), \
        gaussian_filter(dpt.to_numpy(Bz_sub), sigma=1)

    # **Optimized Normalization using oneMKL**
    E_norm = np.sqrt(Ex_sub**2 + Ey_sub**2 + Ez_sub**2)
    E_norm = np.clip(E_norm, 1e-12, max_float)  # Prevent division by zero
    Ex_sub /= E_norm
    Ey_sub /= E_norm
    Ez_sub /= E_norm

    B_norm = np.sqrt(Bx_sub**2 + By_sub**2 + Bz_sub**2)
    B_norm = np.clip(B_norm, 1e-12, max_float)  # Prevent division by zero
    Bx_sub /= B_norm
    By_sub /= B_norm
    Bz_sub /= B_norm

    # **Remove Old Quiver Plots Before Updating**
    if quiver_E is not None:
        quiver_E.remove()
    if quiver_B is not None:
        quiver_B.remove()

    # **Update quiver plot dynamically**
    quiver_E = ax.quiver(X_sub, Y_sub, Z_sub, Ex_sub, Ey_sub, Ez_sub,
                         length=0.2, color='r', alpha=0.7, normalize=True, label="Electric Field")
    quiver_B = ax.quiver(X_sub, Y_sub, Z_sub, Bx_sub, By_sub, Bz_sub,
                         length=0.2, color='b', alpha=0.5, normalize=True, label="Magnetic Field")

    return quiver_E, quiver_B

# **Run the animation**
ani = animation.FuncAnimation(fig, update, frames=time_steps, interval=50, blit=False)

# **Ensure Matplotlib Keeps the Window Open**
plt.show(block=True)


############################################################################################################


