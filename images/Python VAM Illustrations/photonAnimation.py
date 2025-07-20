import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Simulation Parameters
wavelength = 0.5        # Wavelength of vortex irrotational envelope (in arbitrary units)
slit_distance = 2.0     # Distance between slits
screen_distance = 5.0   # Distance to screen
x_range = np.linspace(-10, 10, 800)  # Observation screen (x-axis)
y = screen_distance

# Calculate interference pattern (time-dependent)
def pressure_field(x, t, A=1.0):
    k = 2 * np.pi / wavelength
    r1 = np.sqrt((x + slit_distance / 2) ** 2 + y ** 2)
    r2 = np.sqrt((x - slit_distance / 2) ** 2 + y ** 2)
    v = A * (np.cos(k * r1 - t) + np.cos(k * r2 - t))
    P = -0.5 * v**2  # Bernoulli pressure field (scaled)
    return P

# Create animation
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlim(x_range.min(), x_range.max())
ax.set_ylim(-1.5, 0.2)
ax.set_title("VAM Double-Slit Æther Pressure Field")
ax.set_xlabel("Position on Screen (x)")
ax.set_ylabel("Relative Pressure")

def init():
    line.set_data([], [])
    return line,

def animate(t):
    P = pressure_field(x_range, t)
    line.set_data(x_range, P)
    return line,

ani = animation.FuncAnimation(fig, animate, frames=np.linspace(0, 2*np.pi, 100),
                              init_func=init, blit=True, interval=60)

# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create a 2D grid of points
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)

# Define the vortex-like velocity field
def velocity_field(t):
    u = -Y / (X**2 + Y**2 + 0.1) * np.sin(0.5 * t)
    v = X / (X**2 + Y**2 + 0.1) * np.cos(0.5 * t)
    return u, v

# === Static Snapshot at t = 5 ===
def plot_snapshot(t_snapshot=5):
    u, v = velocity_field(t_snapshot)
    plt.figure(figsize=(6, 6))
    plt.quiver(X, Y, u, v, scale=40, color='teal')
    plt.title(f"Snapshot of Vorticial Flow Field (t = {t_snapshot})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Animated Flow Field ===
def animate_flow():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title("Vorticial Flow Animation")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    quiver = ax.quiver(X, Y, np.zeros_like(X), np.zeros_like(Y), scale=40)

    def update(t):
        u, v = velocity_field(t)
        quiver.set_UVC(u, v)
        return quiver,

    ani = animation.FuncAnimation(fig, update, frames=60, interval=100, blit=False)
    import os
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    filename = f"{script_name}.pdf"

    ani.save(filename, writer='ffmpeg', fps=10)
    # ✅ Get the script filename dynamically and save as pdf


    plt.tight_layout()
    plt.show()

# === Main ===
if __name__ == "__main__":
    plot_snapshot(t_snapshot=5)      # Show static snapshot
    animate_flow()                   # Generate and show animation

