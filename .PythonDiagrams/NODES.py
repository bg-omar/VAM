import matplotlib

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -------------------------------------------------
# Helper functions
# -------------------------------------------------
def biot_savart_velocity(x_eval, X_fil, eps=0.05):
    vel = np.zeros(3)
    gamma = 1.0
    for k in range(len(X_fil) - 1):
        r1 = X_fil[k]
        r2 = X_fil[k + 1]
        dL = r2 - r1
        rm = 0.5 * (r1 + r2)
        R = x_eval - rm
        rnorm_sq = (R @ R + eps ** 2)
        crossval = np.cross(dL, R)
        vel += gamma * crossval / (rnorm_sq ** 1.5)
    vel *= 1.0 / (4.0 * np.pi)
    return vel

def update_vortex_positions(X_fil, dt, eps=0.05):
    N = len(X_fil)
    X_new = np.zeros_like(X_fil)
    for i in range(N):
        xi = X_fil[i]
        v_i = biot_savart_velocity(xi, X_fil, eps)
        X_new[i] = xi + dt * v_i
    return X_new

def make_ring(R=1.0, z0=0.0, npoints=100):
    angles = np.linspace(0, 2 * np.pi, npoints, endpoint=False)
    x = R * np.cos(angles)
    y = R * np.sin(angles)
    z = z0 * np.ones_like(x)
    X_ring = np.vstack([x, y, z]).T
    X_ring = np.vstack([X_ring, X_ring[0]])
    return X_ring

# -------------------------------------------------
# Main demonstration
# -------------------------------------------------
def main_sim():
    R = 1.0
    sep = 2.5
    npoints = 200
    ring1 = make_ring(R=R, z0=+sep / 2, npoints=npoints)
    ring2 = make_ring(R=R, z0=-sep / 2, npoints=npoints)
    dt = 0.01
    nsteps = 300

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')

    def update(step):
            ax.clear()
            ax.set_title(f"Vortex Rings, step={step}")
            ax.plot(ring1[:, 0], ring1[:, 1], ring1[:, 2], 'r.-', label='Ring A')
            ax.plot(ring2[:, 0], ring2[:, 1], ring2[:, 2], 'b.-', label='Ring B')
            ax.set_xlim(-2.0, 2.0)
            ax.set_ylim(-2.0, 2.0)
            ax.set_zlim(-2.0, 2.0)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')


            for ring in [ring1, ring2]:
                ring[:] = update_vortex_positions(ring, dt, eps=0.05)
                ring[-1] = ring[0]

    ani = FuncAnimation(fig, update, frames=nsteps + 1, interval=50)
    plt.show()

if __name__ == "__main__":
    main_sim()