import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

######################################################################################
# Constants
mu_0 = 4 * np.pi * 1e-7  # Vacuum permeability (T·m/A)
epsilon_0 = 8.854e-12
I = 10  # Coil current in Amperes

# Coil parameters (Smaller for better visibility)
R, r = 1.0, 0.5  # 🔥 Shrunk Major and Minor Radius
num_turns = 12   # Total turns per phase
num_points = 600  # Resolution of the coil

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

# Compute Current Density (J) as Directional Vectors Along Coil
def compute_current_vectors(coil_x, coil_y, coil_z):
    Jx, Jy, Jz = np.gradient(coil_x), np.gradient(coil_y), np.gradient(coil_z)
    return Jx, Jy, Jz

Jx_1, Jy_1, Jz_1 = compute_current_vectors(*coil_1)
Jx_2, Jy_2, Jz_2 = compute_current_vectors(*coil_2)
Jx_3, Jy_3, Jz_3 = compute_current_vectors(*coil_3)

# Create a 3D Grid (🔥 20x20x20 grid size!)
grid_size = 10
x_range = np.linspace(-2, 2, grid_size)
y_range = np.linspace(-2, 2, grid_size)
z_range = np.linspace(-2, 2, grid_size)

X, Y, Z = np.meshgrid(x_range, y_range, z_range)

# Function to Compute Magnetic and Electric Fields (Optimized Vectorized Calculation)
def compute_biot_savart(coil_x, coil_y, coil_z, phase_shift):
    dL = np.gradient(np.array([coil_x, coil_y, coil_z]), axis=1)  # 🔥 Vectorized Coil Segment Calculation
    rx, ry, rz = X[..., np.newaxis] - coil_x, Y[..., np.newaxis] - coil_y, Z[..., np.newaxis] - coil_z
    r3 = (rx**2 + ry**2 + rz**2)**(3/2) + 1e-9  # Avoid division by zero

    # 🔥 Vectorized Cross Product Calculation
    dBx = np.sum(mu_0 * I * (dL[1] * rz - dL[2] * ry) / (4 * np.pi * r3), axis=-1)
    dBy = np.sum(mu_0 * I * (dL[2] * rx - dL[0] * rz) / (4 * np.pi * r3), axis=-1)
    dBz = np.sum(mu_0 * I * (dL[0] * ry - dL[1] * rx) / (4 * np.pi * r3), axis=-1)

    # 🔥 Simulated Electric Field (Alternating current effect)
    dEx = epsilon_0 * np.sin(phase_shift) * dBx
    dEy = epsilon_0 * np.cos(phase_shift) * dBy
    dEz = epsilon_0 * np.sin(phase_shift) * dBz

    return dEx, dEy, dEz, dBx, dBy, dBz

# Compute Field Contributions from Each Coil
fields_1 = compute_biot_savart(*coil_1, phase_shift=0)
fields_2 = compute_biot_savart(*coil_2, phase_shift=2*np.pi/3)
fields_3 = compute_biot_savart(*coil_3, phase_shift=-2*np.pi/3)

# Sum Contributions
Ex_total = fields_1[0] + fields_2[0] + fields_3[0]
Ey_total = fields_1[1] + fields_2[1] + fields_3[1]
Ez_total = fields_1[2] + fields_2[2] + fields_3[2]

Bx_total = fields_1[3] + fields_2[3] + fields_3[3]
By_total = fields_1[4] + fields_2[4] + fields_3[4]
Bz_total = fields_1[5] + fields_2[5] + fields_3[5]

# Normalize vectors for visualization
def normalize_vectors(U, V, W):
    magnitude = np.sqrt(U**2 + V**2 + W**2)
    magnitude = np.clip(magnitude, 1e-9, None)
    return U / magnitude, V / magnitude, W / magnitude

Ex_total, Ey_total, Ez_total = normalize_vectors(Ex_total, Ey_total, Ez_total)
Bx_total, By_total, Bz_total = normalize_vectors(Bx_total, By_total, Bz_total)

# Plot Electric and Magnetic Fields
fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(111, projection='3d')

quiver_E, quiver_B, quiver_J = None, None, None

def update(frame):
    global quiver_E, quiver_B, quiver_J

    # Oscillate Fields with Time
    phase_shift = np.sin(frame * 0.1) * np.pi / 6
    Ex_t, Ey_t, Ez_t = Ex_total * np.cos(phase_shift), Ey_total * np.sin(phase_shift), Ez_total * np.cos(phase_shift)
    Bx_t, By_t, Bz_t = Bx_total * np.sin(phase_shift), By_total * np.cos(phase_shift), Bz_total * np.sin(phase_shift)

    # Remove old arrows
    if quiver_E: quiver_E.remove()
    if quiver_B: quiver_B.remove()
    if quiver_J: quiver_J.remove()

    # Quiver plots
    quiver_E = ax.quiver(X, Y, Z, Ex_t, Ey_t, Ez_t, length=0.15, color='r', normalize=True, label="E-Field", alpha=0.5,linewidth=0.5)
    quiver_B = ax.quiver(X, Y, Z, Bx_t, By_t, Bz_t, length=0.15, color='b', normalize=True, label="B-Field", alpha=0.5,linewidth=0.5)
    quiver_J = ax.quiver(coil_1[0], coil_1[1], coil_1[2], Jx_1, Jy_1, Jz_1, length=0.25, label="J-Field", alpha=1, linewidth=1.5)

    return quiver_E, quiver_B , quiver_J


ax.set_title("E, B, & J Fields of 3-Phase Rodin Coil")

ani = animation.FuncAnimation(fig, update, frames=50, interval=100, blit=False)
plt.show()
