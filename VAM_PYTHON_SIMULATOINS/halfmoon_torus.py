# 3D torus with 18 alternating black/white "moon" tiles
# The "moons" are made as crescent-shaped patches on the torus surface
# by subtracting an offset band from a main band in parameter space.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


# --- helpers ---
def angle_diff(a, b):
    """Smallest signed difference between angles a and b (radians), wrapped to [-pi, pi]."""
    d = (a - b + np.pi) % (2 * np.pi) - np.pi
    return d


# --- torus parameters ---
R = 1.2  # major radius
r = 0.45  # minor radius

# parameter grid
n_t, n_p = 720, 240
theta = np.linspace(0, 2 * np.pi, n_t, endpoint=False)  # around the hole
phi = np.linspace(0, 2 * np.pi, n_p, endpoint=False)  # around the tube
Theta, Phi = np.meshgrid(theta, phi)

# torus surface
X = (R + r * np.cos(Phi)) * np.cos(Theta)
Y = (R + r * np.cos(Phi)) * np.sin(Theta)
Z = r * np.sin(Phi)

# --- "moon" tiling design in parameter space ---
N = 18
dtheta = 2 * np.pi / N

# band widths (tuned for a nice moon-like look)
phi_half = 0.85  # radians; half-height of the band in phi
main_width = 0.90 * dtheta  # primary band width in theta
cut_width = 0.78 * dtheta  # cutout band width
cut_shift = 0.44 * dtheta  # offset of the cutout band along theta
phi_shrink = 0.90  # cutout slightly smaller in phi for a curved "moon"

# prepare plot
fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot(111, projection='3d')

# draw each crescent patch
for k in range(N):
    theta_c = (k + 0.5) * dtheta  # center of segment

    # primary band (rectangle in parameter space)
    band_theta = np.abs(angle_diff(Theta, theta_c)) < (main_width / 2.0)
    band_phi = np.abs(angle_diff(Phi, 0.0)) < phi_half
    main_band = band_theta & band_phi

    # cutout band (shifted)
    cut_theta = np.abs(angle_diff(Theta, theta_c + cut_shift)) < (cut_width / 2.0)
    cut_phi = np.abs(angle_diff(Phi, 0.0)) < (phi_half * phi_shrink)
    cut_band = cut_theta & cut_phi

    crescent = main_band & (~cut_band)

    # mask other points
    Xp = np.where(crescent, X, np.nan)
    Yp = np.where(crescent, Y, np.nan)
    Zp = np.where(crescent, Z, np.nan)

    # alternating black/white
    facecolor = 'k' if (k % 2 == 0) else 'w'
    ax.plot_surface(Xp, Yp, Zp, rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False, color=facecolor)

# aesthetics
ax.set_box_aspect([1, 1, 1])
ax.set_xticks([]);
ax.set_yticks([]);
ax.set_zticks([])
ax.set_xlabel('');
ax.set_ylabel('');
ax.set_zlabel('')
ax.view_init(elev=25, azim=40)
ax.set_title('Torus from 18 crescent ("moon") tiles: 9 black, 9 white')

plt.show()
