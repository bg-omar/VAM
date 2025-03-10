




import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


######################################################################################

# Constants
mu_0 = 4 * np.pi * 1e-7  # Vacuum permeability (T·m/A)
I = 10  # Coil current in Amperes

# Coil parameters
R, r = 1.5, 1.0  # Major and minor radius of the torus
num_turns = 12   # Total turns per phase
num_points = 500  # Resolution of the coil

# Generate Rodin Coil Paths
def generate_rodin_coil(R, r, num_turns, num_points, phase_shift=0):
    theta = np.linspace(0, num_turns * 2 * np.pi, num_points)
    phi = (2 + 2/5) * theta + phase_shift  # Rodin winding ratio with phase shift

    x = (R + r * np.cos(phi)) * np.cos(theta)
    y = (R + r * np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)

    return x, y, z

# Generate 3-phase interwoven coil
coil_1 = generate_rodin_coil(R, r, num_turns, num_points, phase_shift=0)
coil_2 = generate_rodin_coil(R, r, num_turns, num_points, phase_shift=2*np.pi/3)
coil_3 = generate_rodin_coil(R, r, num_turns, num_points, phase_shift=-2*np.pi/3)

# Function to compute magnetic field using Biot-Savart Law
def biot_savart(xc, yc, zc, coil_x, coil_y, coil_z):
    Bx, By, Bz = 0, 0, 0
    dl = np.diff(np.array([coil_x, coil_y, coil_z]), axis=1)  # Coil segments
    for i in range(len(dl[0])):
        rx, ry, rz = xc - coil_x[i], yc - coil_y[i], zc - coil_z[i]
        r3 = (rx**2 + ry**2 + rz**2)**(3/2) + 1e-9  # Avoid division by zero

        dBx = mu_0 * I * (dl[1, i] * rz - dl[2, i] * ry) / (4 * np.pi * r3)
        dBy = mu_0 * I * (dl[2, i] * rx - dl[0, i] * rz) / (4 * np.pi * r3)
        dBz = mu_0 * I * (dl[0, i] * ry - dl[1, i] * rx) / (4 * np.pi * r3)

        Bx += dBx
        By += dBy
        Bz += dBz

    return Bx, By, Bz

# Create a 3D Grid to compute B-field at sample points
grid_size = 10
x_range = np.linspace(-2, 2, grid_size)
y_range = np.linspace(-2, 2, grid_size)
z_range = np.linspace(-2, 2, grid_size)

X, Y, Z = np.meshgrid(x_range, y_range, z_range)
Bx_total, By_total, Bz_total = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)

# Compute Magnetic Field Contributions from each phase
for coil in [coil_1, coil_2, coil_3]:
    for i in range(grid_size):
        for j in range(grid_size):
            for k in range(grid_size):
                Bx, By, Bz = biot_savart(X[i, j, k], Y[i, j, k], Z[i, j, k], *coil)
                Bx_total[i, j, k] += Bx
                By_total[i, j, k] += By
                Bz_total[i, j, k] += Bz

# Normalize vectors for better visualization
B_magnitude = np.sqrt(Bx_total**2 + By_total**2 + Bz_total**2)
Bx_total /= B_magnitude + 1e-9
By_total /= B_magnitude + 1e-9
Bz_total /= B_magnitude + 1e-9

# Plot Magnetic Field Vectors
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, Bx_total, By_total, Bz_total, length=0.2, color='b', normalize=True)

# Plot Rodin Coil
ax.plot(*coil_1, 'r-', linewidth=1, label="Phase 1")
ax.plot(*coil_2, 'g-', linewidth=1, label="Phase 2")
ax.plot(*coil_3, 'b-', linewidth=1, label="Phase 3")

# Set Labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title("3-Phase Rodin Coil Magnetic Field Visualization")
ax.legend()
plt.show()


import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import mu_0, epsilon_0, pi

# Coil parameters
R, r = 1.5, 1.0  # Major & minor radius
num_turns = 12   # Number of turns
L = 2e-6         # Estimated inductance (H)
C = 1e-9         # Estimated capacitance (F)
I_max = 10       # Max coil current (A)
f_res = 1 / (2 * pi * np.sqrt(L * C))  # Resonant frequency

# Time simulation
t = np.linspace(0, 5 / f_res, 1000)  # Simulating 5 oscillation periods
omega_res = 2 * pi * f_res           # Angular frequency
I_t = I_max * np.sin(omega_res * t)  # AC current oscillation

# Compute Magnetic Field Variation Over Time
B_t = mu_0 * I_t / (2 * R)  # Approximate field strength over time
P_B = B_t**2 / (2 * mu_0)   # Magnetic pressure variation

# Plot Results
fig, ax = plt.subplots(2, 1, figsize=(10, 6))
ax[0].plot(t * 1e6, I_t, 'r', label="Current I(t)")
ax[0].set_ylabel("Current (A)")
ax[0].legend()
ax[1].plot(t * 1e6, P_B, 'b', label="Magnetic Pressure P_B(t)")
ax[1].set_ylabel("Pressure (Pa)")
ax[1].legend()
plt.xlabel("Time (μs)")
plt.title("Resonance Effects on Rodin Coil")
plt.show()
