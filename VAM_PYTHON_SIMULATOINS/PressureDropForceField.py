import numpy as np
import matplotlib.pyplot as plt
from numpy import gradient
from mpl_toolkits.mplot3d import Axes3D
import ace_tools_open
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

from VAM_14_Topological_Fluid_Dynamics_Lagrangian.images.constants import alpha

# Constants
rho_mass = 3e18   # mass-equivalent æther density [kg/m³]
rho_fluid = 7e-7  # fluid æther density [kg/m³]

# Grid parameters
N = 50
x = np.linspace(-1.5, 1.5, N)
y = np.linspace(-1.5, 1.5, N)
z = np.linspace(-1.5, 1.5, N)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Define a swirl-like vortex vector field (Rodin-like)
r_squared = X**2 + Y**2 + Z**2 + 1e-8
v_theta = 1 / r_squared
vx = -Y * v_theta
vy = X * v_theta
vz = np.zeros_like(vx)

# Calculate vorticity via curl(velocity)
dx = x[1] - x[0]
dy = y[1] - y[0]
dz = z[1] - z[0]

dvz_dy, dvz_dx, _ = np.gradient(vz, dy, dx, dz, edge_order=2)
dvy_dz, _, dvy_dx = np.gradient(vy, dz, dy, dx, edge_order=2)
_, dvx_dz, dvx_dy = np.gradient(vx, dx, dz, dy, edge_order=2)

omega_x = dvz_dy - dvy_dz
omega_y = dvx_dz - dvz_dx
omega_z = dvy_dx - dvx_dy

omega_mag_sq = omega_x**2 + omega_y**2 + omega_z**2

# Æther pressure field
P_ae = -0.5 * rho_mass * omega_mag_sq

# Pressure force field
dP_dx, dP_dy, dP_dz = np.gradient(P_ae, dx, dy, dz, edge_order=2)
fx = -dP_dx / rho_fluid
fy = -dP_dy / rho_fluid
fz = -dP_dz / rho_fluid

# Mid-Z slice for visualization
mid_z = N // 2

# Prepare a 2D plot
fig, ax = plt.subplots(figsize=(8, 6))
contour = ax.contourf(X[:, :, mid_z], Y[:, :, mid_z], P_ae[:, :, mid_z], levels=100, cmap='inferno')
ax.quiver(X[::2, ::2, mid_z], Y[::2, ::2, mid_z], fx[::2, ::2, mid_z], fy[::2, ::2, mid_z],
          color='cyan', scale=1e25, width=0.003, alpha=0.5)
ax.set_title("VAM Æther Pressure Drop and Force Field (Mid-Z Slice)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
fig.colorbar(contour, label="Pressure [Pa]")

plt.tight_layout()

# Convert data to display in a dataframe summary
import pandas as pd
df_summary = pd.DataFrame({
    "Center Pressure (Pa)": [P_ae[N//2, N//2, mid_z]],
    "Center Force Magnitude (N/kg)": [np.sqrt(fx[N//2, N//2, mid_z]**2 + fy[N//2, N//2, mid_z]**2)]
})

ace_tools_open.display_dataframe_to_user(name="VAM Æther Pressure Drop Summary", dataframe=df_summary)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.constants import c

# ──────────────────────────────────────────────────────────────────────────────
# 1. VAM constants (in SI units)
# ──────────────────────────────────────────────────────────────────────────────
rho_mass  = 3e18            # ρ_ae^(mass)  [kg m⁻³]
rho_fluid = 7e-7            # ρ_ae^(fluid) [kg m⁻³]
r_c       = 1.409e-15       # vortex‑core radius [m]
C_e       = 1.09384563e6    # core swirl velocity Ce [m s⁻¹]

# ──────────────────────────────────────────────────────────────────────────────
# 2. Cartesian grid
# ──────────────────────────────────────────────────────────────────────────────
N   = 60                 # grid points per dimension
L   = 1.0e-2             # box half‑width [m] (large compared to r_c)
axes = np.linspace(-L, L, N)
dx   = axes[1] - axes[0]
X, Y, Z = np.meshgrid(axes, axes, axes, indexing='ij')

# radial distance (avoid division by zero)
r2 = X**2 + Y**2 + Z**2
r  = np.sqrt(r2 + 1e-30)

# ──────────────────────────────────────────────────────────────────────────────
# 3. Smooth finite‑core swirl profile
#    v_θ(r) = Ce * r_c² / (r_c² + r²)
# ──────────────────────────────────────────────────────────────────────────────
v_theta = C_e * r_c**2 / (r_c**2 + r2)

# Tangential components in Cartesian coordinates
vx = -v_theta * Y / r
vy =  v_theta * X / r
vz = np.zeros_like(vx)

# ensure finite at the origin
vx[r == 0] = 0.0
vy[r == 0] = 0.0

# ──────────────────────────────────────────────────────────────────────────────
# 4. Vorticity ω = ∇ × v  (central differences, correct spacing order)
# ──────────────────────────────────────────────────────────────────────────────
dvx_dx, dvx_dy, dvx_dz = np.gradient(vx, dx, dx, dx, edge_order=2)
dvy_dx, dvy_dy, dvy_dz = np.gradient(vy, dx, dx, dx, edge_order=2)
dvz_dx, dvz_dy, dvz_dz = np.gradient(vz, dx, dx, dx, edge_order=2)

omega_x = dvz_dy - dvy_dz
omega_y = dvx_dz - dvz_dx
omega_z = dvy_dx - dvx_dy
omega_mag = np.sqrt(omega_x**2 + omega_y**2 + omega_z**2)

# ──────────────────────────────────────────────────────────────────────────────
# 5. Æther pressure and pressure‑gradient force
# ──────────────────────────────────────────────────────────────────────────────
P_ae = -0.5 * rho_mass * omega_mag**2          # Bernoulli‑like pressure
dP_dx, dP_dy, dP_dz = np.gradient(P_ae, dx, dx, dx, edge_order=2)
fx = -dP_dx / rho_fluid
fy = -dP_dy / rho_fluid
fz = -dP_dz / rho_fluid
f_mag = np.sqrt(fx**2 + fy**2 + fz**2)

# ──────────────────────────────────────────────────────────────────────────────
# 6. Extract mid‑plane (Z≈0) for visualisation
# ──────────────────────────────────────────────────────────────────────────────
mid   = N // 2
X2d   = X[:, :, mid]
Y2d   = Y[:, :, mid]
P2d   = P_ae[:, :, mid]
fx2d  = fx[:, :, mid]
fy2d  = fy[:, :, mid]

# colour scale robust statistics
vmin = np.percentile(P2d, 5)
vmax = np.percentile(P2d, 95)

fig, ax = plt.subplots(figsize=(6, 6))
c = ax.contourf(X2d*1e3, Y2d*1e3, P2d, levels=120, vmin=vmin, vmax=vmax)
q = ax.quiver(X2d*1e3, Y2d*1e3, fx2d, fy2d, scale=1e21, width=0.002)
ax.set_title("VAM swirl‑induced æther pressure drop (mid‑plane)")
ax.set_xlabel("x [mm]")
ax.set_ylabel("y [mm]")
fig.colorbar(c, ax=ax, label="Pressure [Pa]")
plt.tight_layout()

# ──────────────────────────────────────────────────────────────────────────────
# 7. Diagnostics table
# ──────────────────────────────────────────────────────────────────────────────
centre = (N//2, N//2, N//2)
centre_pressure = P_ae[centre]
centre_force    = f_mag[centre]

df = pd.DataFrame(
    {
        "Quantity": ["Centre pressure", "Centre |f|"],
        "Value (SI units)": [centre_pressure, centre_force],
        "Units": ["Pa", "m s⁻²"],
    }
)
import ace_tools_open as tools; tools.display_dataframe_to_user("VAM swirl diagnostics", df)

# Generate a richer visual: mid‑plane pressure map + 1‑D radial profile
import numpy as np, matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# --- use existing arrays from previous cell ---
mid = X.shape[2]//2
X2d = X[:, :, mid]*1e3   # mm
Y2d = Y[:, :, mid]*1e3
P2d = P_ae[:, :, mid]
fx2d = fx[:, :, mid]
fy2d = fy[:, :, mid]

# radial line along x‑axis (y=0, z=0)
line_idx = np.argmin(np.abs(Y[:,0,0]))    # index closest to y=0
P_line  = P_ae[:, line_idx, mid]
f_line  = f_mag[:, line_idx, mid]
r_line  = np.abs(X[:, line_idx, mid])

# --- plotting ---
fig = plt.figure(figsize=(12,5))
gs  = GridSpec(1,2, width_ratios=[1.1,1])

# (a) 2‑D pressure map with force vectors
ax0 = fig.add_subplot(gs[0])
cmap = ax0.contourf(X2d, Y2d, P2d, 150, cmap='viridis')
q    = ax0.quiver(X2d, Y2d, fx2d, fy2d, color='white', scale=1e21, width=0.002)
ax0.set_title("Mid‑plane pressure drop & force\n(VAM finite‑core swirl)")
ax0.set_xlabel("x [mm]"); ax0.set_ylabel("y [mm]")
fig.colorbar(cmap, ax=ax0, label="Pressure [Pa]")

# (b) radial profile
ax1 = fig.add_subplot(gs[1])
ax1.plot(r_line*1e3, P_line, label="Pressure")
ax1.set_xlabel("r [mm]")
ax1.set_ylabel("Pressure [Pa]", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.plot(r_line*1e3, f_line, color='tab:red', label="|f|")
ax2.set_ylabel("|f| [m s⁻²]", color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

ax1.set_title("Radial profile (y=0, z=0)")
ax1.grid(True)
fig.tight_layout()
fig.show()

