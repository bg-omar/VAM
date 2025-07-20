
import matplotlib.animation as animation
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # gravitational constant, m^3/kg/s^2
M = 5.972e24     # mass of Earth, kg
c = 3.0e8        # speed of light, m/s

# Generate grid of radii (r) and orbital velocities (v)
r = np.linspace(6.4e6, 1.0e8, 200)  # from Earth's radius to far orbit
v = np.linspace(0, 1.0e7, 200)      # orbital velocities up to ~10,000 km/s

R, V = np.meshgrid(r, v)

# Gravitational inflow velocity (vg) and orbital velocity (vorb)
vg = np.sqrt(2 * G * M / R)
vrel = np.sqrt(V**2 + vg**2)  # Combined relative velocity (vector sum)

# Time dilation factor: dτ/dt = sqrt(1 - v_rel^2 / c^2)
time_dilation = np.sqrt(1 - (vrel**2) / c**2)
time_dilation = np.clip(time_dilation, 0, 1)  # prevent complex values


# Setup: Create a grid and define mass locations
grid_size = 100
x = np.linspace(-5e7, 5e7, grid_size)
y = np.linspace(-5e7, 5e7, grid_size)
X, Y = np.meshgrid(x, y)

# Define masses at fixed positions
mass_positions = [(-2e7, 0), (2e7, 0)]
mass_strengths = [G * M, G * M]

# Function to compute æther inflow velocity vectors at each point
def compute_ether_flow(X, Y, mass_positions, mass_strengths):
    u = np.zeros_like(X)
    v = np.zeros_like(Y)
    for (mx, my), strength in zip(mass_positions, mass_strengths):
        dx = X - mx
        dy = Y - my
        r2 = dx**2 + dy**2 + 1e6  # avoid div by 0
        r = np.sqrt(r2)
        factor = strength / r2
        u -= factor * dx / r
        v -= factor * dy / r
    return u, v

# Initialize figure
fig, ax = plt.subplots(figsize=(8, 8))

# Plot setup
quiver = ax.quiver(X, Y, np.zeros_like(X), np.zeros_like(Y), color='blue', pivot='mid')
ax.set_xlim(-5e7, 5e7)
ax.set_ylim(-5e7, 5e7)
ax.set_aspect('equal')
ax.set_title('Animated Æther Flow Around Multiple Masses (VAM)')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')

# Animation update function
def update(frame):
    angle = frame * 2 * np.pi / 60
    # Rotate mass positions in a circle
    r_mass = 2e7
    mass_positions_rot = [
        (r_mass * np.cos(angle), r_mass * np.sin(angle)),
        (-r_mass * np.cos(angle), -r_mass * np.sin(angle))
    ]
    u, v = compute_ether_flow(X, Y, mass_positions_rot, mass_strengths)
    quiver.set_UVC(u, v)
    return quiver,

# Create animation
ani = animation.FuncAnimation(fig, update, frames=60, interval=100, blit=True)

# Display animation
plt.close()
# Display animation interactively
plt.show()

# Save animation as a GIF
ani.save(filename="Animate.gif", writer='imagemagick', fps=10)

# Re-import necessary libraries after kernel reset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Re-define constants
G = 6.67430e-11  # gravitational constant, m^3/kg/s^2
M = 5.972e24     # mass of Earth, kg

# Grid setup
grid_size = 100
x = np.linspace(-5e7, 5e7, grid_size)
y = np.linspace(-5e7, 5e7, grid_size)
X, Y = np.meshgrid(x, y)

# Function to compute æther inflow velocity vectors at each point
def compute_ether_flow(X, Y, mass_positions, mass_strengths):
    u = np.zeros_like(X)
    v = np.zeros_like(Y)
    for (mx, my), strength in zip(mass_positions, mass_strengths):
        dx = X - mx
        dy = Y - my
        r2 = dx**2 + dy**2 + 1e6  # avoid division by zero
        r = np.sqrt(r2)
        factor = strength / r2
        u -= factor * dx / r
        v -= factor * dy / r
    return u, v

# Mass configuration: Two fixed, one orbiting above center
mass_positions_lag = [(-2e7, 0), (2e7, 0), (0, 3.5e7)]
mass_strengths_lag = [G * M, G * M, G * M]

# Initialize figure
fig_lag, ax_lag = plt.subplots(figsize=(8, 8))
quiver_lag = ax_lag.quiver(X, Y, np.zeros_like(X), np.zeros_like(Y), color='darkblue', pivot='mid')
ax_lag.set_xlim(-5e7, 5e7)
ax_lag.set_ylim(-5e7, 5e7)
ax_lag.set_aspect('equal')
ax_lag.set_title('Æther Flow Around Three Masses (VAM with Vortex Interference)')
ax_lag.set_xlabel('x (m)')
ax_lag.set_ylabel('y (m)')

# Animation update function for triple-mass system
def update_lag(frame):
    angle = frame * 2 * np.pi / 60
    r3 = 3.5e7
    x3 = r3 * np.cos(angle)
    y3 = r3 * np.sin(angle)
    mass_positions_rot = [(-2e7, 0), (2e7, 0), (x3, y3)]
    u, v = compute_ether_flow(X, Y, mass_positions_rot, mass_strengths_lag)
    quiver_lag.set_UVC(u, v)
    return quiver_lag,

# Create animation
ani_lag = animation.FuncAnimation(fig_lag, update_lag, frames=60, interval=100, blit=True)

# Display animation
plt.close()
plt.show()

# Save animation as a GIF
ani_lag.save(filename="Animate-3.gif", writer='imagemagick', fps=10)
