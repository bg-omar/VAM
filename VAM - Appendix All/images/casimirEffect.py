import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Parameters for Casimir-style mode suppression visualization
plate_separation = np.linspace(1e-9, 1e-6, 500)  # meters
max_mode = 1e9  # max allowed virtual mode frequency in Hz
c = 3e8  # speed of light (used symbolically here)

# Mode suppression: assume inverse square scaling (simplified)
suppressed_modes = (1 / plate_separation**2) / (1 / plate_separation[0]**2)

# Pressure is proportional to suppressed virtual mode density
pressure = suppressed_modes * 1e-3  # arbitrary units

# Plot
plt.figure(figsize=(10, 5))
plt.plot(plate_separation * 1e9, pressure, label='VAM Virtual Mode Pressure', color='purple')
plt.xlabel('Plate Separation (nm)')
plt.ylabel('Relative Pressure (a.u.)')
plt.title('Casimir-Like Pressure from Swirl Mode Suppression in VAM')
plt.grid(True)
plt.legend()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 5))

# Panel A: Refractive Index vs Radius
ax1 = fig.add_subplot(1, 2, 1)
radius = np.linspace(0.1, 3, 500)
n_effective = 1 + 0.4 * np.exp(-radius / 0.8)

ax1.plot(radius, n_effective, color='royalblue', linewidth=2)
ax1.set_title('A: Lensing - Effective Refractive Index vs Radius')
ax1.set_xlabel('Radius (km)')
ax1.set_ylabel('Refractive Index')
ax1.grid(True)

# Panel B: Entangled Vortex Loops
ax2 = fig.add_subplot(1, 2, 2, projection='3d')

# Parametric vortex loops (linked torus knots)
t = np.linspace(0, 2 * np.pi, 500)
x1 = np.sin(t)
y1 = np.cos(t)
z1 = np.sin(2 * t)

x2 = np.sin(t + np.pi)
y2 = np.cos(t + np.pi)
z2 = -np.sin(2 * t)

ax2.plot3D(x1, y1, z1, color='mediumorchid', linewidth=3)
ax2.plot3D(x2, y2, z2, color='mediumslateblue', linewidth=3)

ax2.set_title('B: Entangled Twist-Linked Vortex Structures')
ax2.axis('off')

plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}2.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()


import numpy as np
import matplotlib.pyplot as plt

# Grid
x, y = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
r = np.sqrt(x**2 + y**2) + 1e-5  # avoid divide by zero

# Radial inflow + angular swirl field
v_r = -x / r**2
v_theta = y / r**2
u = v_r - v_theta  # x-component
v = -y / r**2 - x / r**2  # y-component

# Plot streamlines
plt.figure(figsize=(6, 6))
plt.streamplot(x, y, u, v, color=np.sqrt(u**2 + v**2), linewidth=1.5, cmap='plasma')
plt.title("2D Vortex Inflow Field Lines")
plt.xlabel("x")
plt.ylabel("y")
plt.axis('equal')
plt.grid(False)
plt.tight_layout()
filename = f"{script_name}3.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Helix
theta = np.linspace(0, 8 * np.pi, 1000)
z = np.linspace(-2, 2, 1000)
x = np.cos(theta)
y = np.sin(theta)

# Define tension field (arbitrary: tension increases with curvature)
tension = np.abs(np.sin(3 * theta)) + 0.2

# Plotting
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, linewidth=3, color='gray', alpha=0.3)

# Colored tension segments
for i in range(len(x)-1):
    ax.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=plt.cm.plasma(tension[i]), linewidth=2)

ax.set_title("3D Vortex Swirl Colored by Tension")
ax.axis('off')
plt.tight_layout()
filename = f"{script_name}4.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Grid
x, y = np.meshgrid(np.linspace(-4, 4, 100), np.linspace(-4, 4, 100))
r = np.sqrt(x**2 + y**2) + 1e-5

# Æther flow: radial inflow with rotational swirl
u = (-x + y) / r**2
v = (-y - x) / r**2

# Particle positions
num_particles = 30
angles = np.linspace(0, 2*np.pi, num_particles)
r0 = 3.5
px = r0 * np.cos(angles)
py = r0 * np.sin(angles)

fig, ax = plt.subplots(figsize=(6, 6))
stream = ax.streamplot(x, y, u, v, color='lightgray', linewidth=0.5)
particles, = ax.plot(px, py, 'ro', markersize=3)

def update(frame):
    global px, py
    for i in range(num_particles):
        ix = np.argmin(np.abs(x[0] - px[i]))
        iy = np.argmin(np.abs(y[:, 0] - py[i]))
        vx = u[iy, ix]
        vy = v[iy, ix]
        px[i] += vx * 0.1
        py[i] += vy * 0.1
    particles.set_data(px, py)
    return particles,

ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_title("Test Particles Dragged by Æther Swirl Field")
ax.set_aspect('equal')
ax.axis('off')

anim = FuncAnimation(fig, update, frames=200, interval=50)
filename = f"{script_name}5.gif"
anim.save(filename, fps=20)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

t = np.linspace(0, 2*np.pi, 400)
r = 1.0

# Two linked vortex loops
x1 = r * np.cos(t)
y1 = r * np.sin(t)
z1 = 0.3 * np.sin(3*t)

x2 = r * np.sin(t)
y2 = 0.3 * np.sin(3*t)
z2 = r * np.cos(t)

line1, = ax.plot(x1, y1, z1, color='orchid', lw=2)
line2, = ax.plot(x2, y2, z2, color='skyblue', lw=2)

def update(frame):
    phi = frame / 20.0
    twist = np.sin(phi)
    line1.set_data(r * np.cos(t), r * np.sin(t))
    line1.set_3d_properties(0.3 * np.sin(3*t + twist))

    line2.set_data(r * np.sin(t + twist), 0.3 * np.sin(3*t))
    line2.set_3d_properties(r * np.cos(t + twist))
    return line1, line2

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
ax.axis('off')
ax.set_title("Vortex Reconnection Dance")

ani = FuncAnimation(fig, update, frames=100, interval=60)
filename = f"{script_name}6.gif"
ani.save(filename, fps=20)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(9, 6))
ax = fig.add_subplot(111, projection='3d')

# Trefoil knot parametric
t = np.linspace(0, 2*np.pi, 800)
x1 = np.sin(t) + 2*np.sin(2*t)
y1 = np.cos(t) - 2*np.cos(2*t)
z1 = -np.sin(3*t)

# Clone & rotate second vortex (braid)
x2 = -np.sin(t + np.pi/2) - 2*np.sin(2*t + np.pi/3)
y2 = -np.cos(t + np.pi/2) + 2*np.cos(2*t + np.pi/3)
z2 = np.sin(3*t + np.pi/4)

line1, = ax.plot([], [], [], color='orange', lw=2, alpha=0.9)
line2, = ax.plot([], [], [], color='cyan', lw=2, alpha=0.9)

def update(frame):
    phase = frame * 0.1
    twist = np.sin(2*t + phase)

    # Apply phase/twist deformations
    line1.set_data(x1 + 0.3*np.sin(t + phase), y1 + 0.3*np.cos(t + phase))
    line1.set_3d_properties(z1 + 0.5 * twist)

    line2.set_data(x2 - 0.3*np.cos(t - phase), y2 - 0.3*np.sin(t - phase))
    line2.set_3d_properties(z2 - 0.5 * twist)
    return line1, line2

ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_zlim(-4, 4)
ax.axis('off')
ax.set_title("Nonlinear Topological Vortex Reconnection")

ani = FuncAnimation(fig, update, frames=120, interval=60)
filename = f"{script_name}7.gif"
ani.save(filename, fps=20)
plt.show()






