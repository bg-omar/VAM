# NOTE: This code requires a desktop Python environment with matplotlib and numpy installed.
# To install dependencies: pip install matplotlib numpy


import matplotlib
matplotlib.use("TkAgg")
# NOTE: This code requires a desktop Python environment with matplotlib and numpy installed.
# To install dependencies: pip install matplotlib numpy
# NOTE: This code requires a desktop Python environment with matplotlib and numpy installed.
# To install dependencies: pip install matplotlib numpy

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Slider, CheckButtons
from scipy.constants import mu_0

fig = plt.figure(figsize=(10, 8))
plt.subplots_adjust(left=0.25, bottom=0.45)
ax = fig.add_subplot(111, projection='3d')

# === Dipole Ring Generator ===
def generate_ring(num_magnets, radius, toroidal_degrees, poloidal_degrees):
    positions = []
    orientations = []
    for i in range(num_magnets):
        phi = 2 * np.pi * i / num_magnets
        x, y, z = radius * np.cos(phi), radius * np.sin(phi), 0.0
        positions.append(np.array([x, y, z]))

        toroidal_angle = np.deg2rad(toroidal_degrees) * i / num_magnets
        poloidal_angle = np.deg2rad(poloidal_degrees) * np.sin(phi)

        mx = np.cos(2 * phi + toroidal_angle)
        my = np.sin(2 * phi + toroidal_angle)
        mz = np.sin(poloidal_angle)

        m = np.array([mx, my, mz])
        m /= np.linalg.norm(m)
        orientations.append(m)
    return positions, orientations

# === Cube Rendering ===
def draw_correctly_aligned_cube(ax, center, direction, size=0.3, north_color='white', south_color='black', side_color='red'):
    direction = direction / np.linalg.norm(direction)
    z_axis = direction
    x_axis = np.cross(z_axis, [0, 0, 1]) if np.linalg.norm(np.cross(z_axis, [0, 0, 1])) > 1e-6 else np.cross(z_axis, [0, 1, 0])
    x_axis /= np.linalg.norm(x_axis)
    y_axis = np.cross(z_axis, x_axis)
    R = np.stack([x_axis, y_axis, z_axis], axis=1)

    d = size / 2
    cube_verts = np.array([[x, y, z] for x in [-d, d] for y in [-d, d] for z in [-d, d]])
    cube_verts = cube_verts @ R.T + center
    faces = [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4],
             [2, 3, 7, 6], [1, 3, 7, 5], [0, 2, 6, 4]]
    local_normals = np.array([[0, 0, -1], [0, 0, 1], [0, -1, 0],
                              [0, 1, 0], [1, 0, 0], [-1, 0, 0]])
    world_normals = local_normals @ R.T
    dots = np.dot(world_normals, direction)
    north_idx = np.argmax(dots)
    south_idx = np.argmin(dots)
    poly3d = [[cube_verts[idx] for idx in face] for face in faces]
    face_colors_map = [north_color if i == north_idx else south_color if i == south_idx else side_color for i in range(6)]
    ax.add_collection3d(Poly3DCollection(poly3d, facecolors=face_colors_map, edgecolors='k'))

# === Interactive Plot ===
def update_plot(num_magnets, radius, toroidal_deg, poloidal_deg):
    ax.cla()
    ax.set_title(f"Dipole Ring: {num_magnets} magnets")

    positions, orientations = generate_ring(num_magnets, radius, toroidal_deg, poloidal_deg)
    winding_colors = np.linspace(0, 1, num_magnets, endpoint=False)

    for pos, ori, c in zip(positions, orientations, winding_colors):
        if show_cubes[0]:
            draw_correctly_aligned_cube(ax, pos, ori, size=cube_size[0])
        if show_arrows[0]:
            start = pos - ori * cube_size[0] * 0.5
            ax.quiver(*start, *ori, length=cube_size[0], color=plt.cm.hsv(c), linewidth=2, arrow_length_ratio=0.25, normalize=False)

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_zlim(-2, 2)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_box_aspect([1, 1, 1])
    fig.canvas.draw_idle()

# Initial parameters
num_magnets_0 = 16
radius_0 = 1.5
toroid_0 = 720
poloid_0 = 90
show_cubes = [True]
show_arrows = [True]
cube_size = [0.3]

update_plot(num_magnets_0, radius_0, toroid_0, poloid_0)

# Slider axes
axcolor = 'lightgoldenrodyellow'
ax_num = plt.axes([0.25, 0.35, 0.65, 0.03], facecolor=axcolor)
ax_rad = plt.axes([0.25, 0.3, 0.65, 0.03], facecolor=axcolor)
ax_toroid = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_poloid = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_size = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_checks = plt.axes([0.025, 0.4, 0.15, 0.1], facecolor='lightgrey')

# Sliders
s_num = Slider(ax_num, 'Magnets', 2, 64, valinit=num_magnets_0, valstep=1)
s_rad = Slider(ax_rad, 'Radius', 0.5, 5.0, valinit=radius_0, valstep=0.1)
s_toroid = Slider(ax_toroid, 'Toroid (°)', 0, 1440, valinit=toroid_0, valstep=90)
s_poloid = Slider(ax_poloid, 'Poloid (°)', 0, 720, valinit=poloid_0, valstep=15)
s_size = Slider(ax_size, 'Size', 0.1, 0.8, valinit=cube_size[0], valstep=0.05)

checks = CheckButtons(ax_checks, ['Show Cubes', 'Show Arrows'], [True, True])

# Update callback
def slider_update(val):
    cube_size[0] = s_size.val
    update_plot(int(s_num.val), s_rad.val, s_toroid.val, s_poloid.val)

def check_update(label):
    if label == 'Show Cubes':
        show_cubes[0] = not show_cubes[0]
    elif label == 'Show Arrows':
        show_arrows[0] = not show_arrows[0]
    update_plot(int(s_num.val), s_rad.val, s_toroid.val, s_poloid.val)

s_num.on_changed(slider_update)
s_rad.on_changed(slider_update)
s_toroid.on_changed(slider_update)
s_poloid.on_changed(slider_update)
s_size.on_changed(slider_update)
checks.on_clicked(check_update)

plt.show()
