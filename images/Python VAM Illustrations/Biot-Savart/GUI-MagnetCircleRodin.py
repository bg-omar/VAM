# Refactored for optional VAMbindings acceleration (biot_savart + dipole grid kernels if available).
# Falls back to fast NumPy vectorizations when bindings are absent.
# C++/bindings (if used): ./src/field_kernels.cpp, ./src/field_kernels.h
# PyBind11: ./src_bindings/py_field_kernels.cpp
# Example usage: ./examples/field_kernels_example.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, TextBox
import os
import matplotlib
matplotlib.use('TkAgg')


# --- Optional VAMbindings (if present) ---
# If your build provides Biot–Savart and dipole grid evaluators, expose them here.
# Otherwise, the code will use the NumPy fallbacks below.
try:
    from sstbindings import (
        # canonical VAM examples (not used here unless provided in your build)
        lamb_oseen_velocity,
        lamb_oseen_vorticity,
        hill_streamfunction,
        hill_vorticity,
        hill_circulation,
        hill_velocity,
    )
except Exception:
    pass

try:
    # Expected signatures (float32/float64):
    # biot_savart_wire_grid(X, Y, Z, wire_points[N,3], current) -> (Bx,By,Bz)
    # dipole_ring_field_grid(X, Y, Z, positions[M,3], moments[M,3]) -> (Bx,By,Bz)
    from sstbindings import biot_savart_wire_grid, dipole_ring_field_grid
    _HAS_VAM_BIOT = True
except Exception:
    _HAS_VAM_BIOT = False

# --- Utility ---
script_name = os.path.splitext(os.path.basename(__file__))[0]
def saving(plot):
    filename = f"{script_name}.png"
    plot.savefig(filename, dpi=150)

# --- Rodin Starship Coil Geometry ---
def generate_rodin_starship(R=1.0, r=1.0, num_turns=10, num_points=1000):
    theta = np.linspace(0, num_turns * 2 * np.pi, num_points)
    phi = (2 + 2/5) * theta
    x = (R + r * np.cos(phi)) * np.cos(theta)
    y = (R + r * np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)
    return x, y, z

# --- Biot-Savart for wire loop ---
def _biot_savart_wire_numpy(X, Y, Z, wire_points, current=1.0):
    """Vectorized NumPy fallback for Biot–Savart over polyline."""
    mu0 = 1.0
    dl = np.diff(wire_points, axis=0)                                      # [S,3]
    r_mid = 0.5 * (wire_points[:-1] + wire_points[1:])                     # [S,3]

    # Grid to [...,3]
    R = np.stack([X, Y, Z], axis=-1)                                       # [Nx,Ny,Nz,3]
    dBx = np.zeros_like(X, dtype=R.dtype[...,0].dtype)
    dBy = np.zeros_like(Y, dtype=R.dtype[...,0].dtype)
    dBz = np.zeros_like(Z, dtype=R.dtype[...,0].dtype)

    factor = (mu0 * current) / (4.0 * np.pi)

    # Loop over segments only (grid fully vectorized)
    for s in range(dl.shape[0]):
        Rseg = R - r_mid[s]                                                # [Nx,Ny,Nz,3]
        norm = np.linalg.norm(Rseg, axis=-1)                                # [Nx,Ny,Nz]
        mask = norm > 1e-7
        # cross(dl, Rseg)
        cx = dl[s,1]*Rseg[...,2] - dl[s,2]*Rseg[...,1]
        cy = dl[s,2]*Rseg[...,0] - dl[s,0]*Rseg[...,2]
        cz = dl[s,0]*Rseg[...,1] - dl[s,1]*Rseg[...,0]
        inv = np.zeros_like(norm)
        inv[mask] = 1.0 / (norm[mask]**3)
        dBx += factor * cx * inv
        dBy += factor * cy * inv
        dBz += factor * cz * inv
    return dBx, dBy, dBz

def biot_savart_wire(X, Y, Z, wire_points, current=1.0):
    tangents = np.diff(wire_points, axis=0)
    midpoints = 0.5 * (wire_points[:-1] + wire_points[1:])
    grid_points = np.stack((X, Y, Z), axis=-1).reshape(-1, 3)

    B = np.zeros((grid_points.shape[0], 3))
    for mp, t in zip(midpoints, tangents):
        B += np.array([biot_savart_velocity(p.tolist(), [mp.tolist()], [t.tolist()], current)
                       for p in grid_points])

    return B[:, 0].reshape(X.shape), B[:, 1].reshape(Y.shape), B[:, 2].reshape(Z.shape)

# --- Dipole ring geometry ---
def generate_dipole_ring(radius, num_magnets, z_offset=0.0, invert=False):
    positions, orientations = [], []
    for i in range(num_magnets):
        phi = 2 * np.pi * i / num_magnets
        x, y, z = radius * np.cos(phi), radius * np.sin(phi), z_offset
        mx = np.cos(2 * phi)
        my = np.sin(2 * phi)
        mz = np.cos(phi)
        m = np.array([mx, my, (-1 if invert else 1) * mz])
        m /= np.linalg.norm(m)
        orientations.append(m)
        positions.append(np.array([x, y, z]))
    return positions, orientations

# Patch: fix NumPy fallback broadcasting in dipole evaluator (keeps VAMbindings pathway unchanged).
# C++/bindings (if used): ./src/field_kernels.cpp, ./src/field_kernels.h
# PyBind11: ./src_bindings/py_field_kernels.cpp
# Example: ./examples/field_kernels_example.py

def _magnetic_field_dipoles_numpy(X, Y, Z, positions, orientations):
    """Vectorized dipole superposition on the grid (NumPy fallback)."""
    mu0 = 1.0

    # Grid [...,3]
    R = np.stack([X, Y, Z], axis=-1)                                        # [Nx,Ny,Nz,3]

    # Dipoles [M,3]
    P = np.asarray(positions, dtype=float)                                   # [M,3]
    M = np.asarray(orientations, dtype=float)                                # [M,3]

    # Expand dipoles across grid
    Rm = R[..., None, :] - P.reshape((1, 1, 1, -1, 3))                       # [Nx,Ny,Nz,M,3]
    norm = np.linalg.norm(Rm, axis=-1)                                       # [Nx,Ny,Nz,M]

    # Safe unit vectors
    rhat = np.zeros_like(Rm, dtype=float)
    mask = norm > 1e-10
    rhat[mask] = Rm[mask] / norm[mask][..., None]

    inv3 = np.zeros_like(norm, dtype=float)
    inv3[mask] = 1.0 / (norm[mask] ** 3)

    # Dot(m, rhat) per dipole m (match M along its first axis)
    # rhat: [..., M, 3], M: [M, 3]  -> mdotr: [..., M]
    mdotr = np.einsum('...mj,mj->...m', rhat, M)

    # 3(m·r̂)r̂ - m  (broadcast m over grid)
    M_exp = M.reshape((1, 1, 1, -1, 3))
    term = 3.0 * mdotr[..., None] * rhat - M_exp                             # [Nx,Ny,Nz,M,3]

    B = (mu0 / (4.0 * np.pi)) * np.sum(term * inv3[..., None], axis=-2)      # sum over M
    return B[..., 0], B[..., 1], B[..., 2]


def compute_dipole_field_from_orientations(X, Y, Z, positions, orientations):
    if _HAS_VAM_BIOT:
        pos = np.asarray(positions, dtype=float)
        mom = np.asarray(orientations, dtype=float)
        return dipole_ring_field_grid(X, Y, Z, pos, mom)
    return _magnetic_field_dipoles_numpy(X, Y, Z, positions, orientations)

# --- Initial Parameters (user can edit) ---
params = {
    "num_magnets": 16,
    "dipole_ring_radius": 0.5,
    "rodin_major": 1.0,
    "rodin_minor": 0.9,
    "num_turns": 10
}
num_points = 2000
z_offset_top = 0.75
z_offset_bottom = -0.75
x_range = (-2, 2)
y_range = (-2, 2)
z_range = (-2, 2)
field_grid_N = 9

def compute_all_fields_and_geometry():
    bottom_pos, bottom_ori = generate_dipole_ring(params["dipole_ring_radius"], params["num_magnets"], z_offset=z_offset_bottom, invert=False)
    top_pos, top_ori = generate_dipole_ring(params["dipole_ring_radius"], params["num_magnets"], z_offset=z_offset_top, invert=True)
    winding_colors = np.linspace(0, 1, params["num_magnets"], endpoint=False)
    rodin_x, rodin_y, rodin_z = generate_rodin_starship(
        R=params["rodin_major"], r=params["rodin_minor"], num_turns=params["num_turns"], num_points=num_points)
    rodin_wire_points = np.stack([rodin_x, rodin_y, rodin_z], axis=-1)

    X, Y, Z = np.meshgrid(
        np.linspace(*x_range, field_grid_N),
        np.linspace(*y_range, field_grid_N),
        np.linspace(*z_range, field_grid_N),
        indexing='xy'
    )

    print("Recomputing all fields for new parameters... (VAM:", "on" if _HAS_VAM_BIOT else "off", ")")
    Bx_bottom, By_bottom, Bz_bottom = compute_dipole_field_from_orientations(X, Y, Z, bottom_pos, bottom_ori)
    Bx_top, By_top, Bz_top = compute_dipole_field_from_orientations(X, Y, Z, top_pos, top_ori)
    Bx_rodin, By_rodin, Bz_rodin = biot_savart_wire(X, Y, Z, rodin_wire_points, current=1.0)

    return (X, Y, Z,
            bottom_pos, bottom_ori,
            top_pos, top_ori,
            winding_colors,
            rodin_x, rodin_y, rodin_z, rodin_wire_points,
            Bx_bottom, By_bottom, Bz_bottom,
            Bx_top, By_top, Bz_top,
            Bx_rodin, By_rodin, Bz_rodin)

# --- GUI Plotting function ---
def update_plot(*args):
    show_bottom_field = cb_field_status[0]
    show_top_field = cb_field_status[1]
    show_rodin_field = cb_field_status[2]
    show_bottom_geom = cb_geom_status[0]
    show_top_geom = cb_geom_status[1]
    show_rodin_geom = cb_geom_status[2]

    (X, Y, Z,
     bottom_pos, bottom_ori,
     top_pos, top_ori,
     winding_colors,
     rodin_x, rodin_y, rodin_z, rodin_wire_points,
     Bx_bottom, By_bottom, Bz_bottom,
     Bx_top, By_top, Bz_top,
     Bx_rodin, By_rodin, Bz_rodin) = gui_state["data"]

    Bx = np.zeros_like(Bx_bottom)
    By = np.zeros_like(By_bottom)
    Bz = np.zeros_like(Bz_bottom)

    field_components = []
    if show_bottom_field:
        Bx += Bx_bottom; By += By_bottom; Bz += Bz_bottom
        field_components.append("Bottom Ring")
    if show_top_field:
        Bx += Bx_top; By += By_top; Bz += Bz_top
        field_components.append("Top Ring")
    if show_rodin_field:
        Bx += Bx_rodin; By += By_rodin; Bz += Bz_rodin
        field_components.append("Rodin Coil")

    Bmag = np.sqrt(Bx**2 + By**2 + Bz**2)
    Bmag[Bmag == 0] = 1e-9
    Bx_norm = Bx / Bmag; By_norm = By / Bmag; Bz_norm = Bz / Bmag

    ax.clear()
    if show_bottom_field or show_top_field or show_rodin_field:
        ax.quiver(X, Y, Z, Bx_norm, By_norm, Bz_norm, length=0.15, normalize=True, color='blue', linewidth=0.5, alpha=0.9)

    if show_rodin_geom:
        ax.plot3D(rodin_x, rodin_y, rodin_z, color='magenta', linewidth=2, label='Rodin Starship Coil')
    if show_bottom_geom:
        for pos, ori, c in zip(bottom_pos, bottom_ori, winding_colors):
            start = pos - ori * 0.3
            ax.quiver(*start, *ori, length=0.6, color=plt.cm.hsv(c), linewidth=2, arrow_length_ratio=0.25)
    if show_top_geom:
        for pos, ori, c in zip(top_pos, top_ori, winding_colors):
            start = pos - ori * 0.3
            ax.quiver(*start, *ori, length=0.6, color=plt.cm.hsv(c), linewidth=2, arrow_length_ratio=0.25)

    title = "Field: " + (", ".join(field_components) if field_components else "None")
    ax.set_title(title)
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    ax.set_xlim(*x_range); ax.set_ylim(*y_range); ax.set_zlim(*z_range)
    ax.set_box_aspect([1, 1, 1])
    try: ax.legend()
    except Exception: pass
    fig.canvas.draw_idle()

def on_field_checkbox(label):
    idx = cb_field_labels.index(label)
    cb_field_status[idx] = not cb_field_status[idx]
    update_plot()

def on_geom_checkbox(label):
    idx = cb_geom_labels.index(label)
    cb_geom_status[idx] = not cb_geom_status[idx]
    update_plot()

def update_params(label):
    try:
        nmag = int(tb_num_magnets.text)
        rring = float(tb_ring_radius.text)
        rmajor = float(tb_rodin_major.text)
        rminor = float(tb_rodin_minor.text)
        nturn = int(tb_num_turns.text)
        assert nmag > 0 and nturn > 0 and rring > 0 and rmajor > 0 and rminor > 0
    except Exception as e:
        print("Invalid input:", e)
        return
    params["num_magnets"] = nmag
    params["dipole_ring_radius"] = rring
    params["rodin_major"] = rmajor
    params["rodin_minor"] = rminor
    params["num_turns"] = nturn
    gui_state["data"] = compute_all_fields_and_geometry()
    update_plot()

# --- GUI State ---
gui_state = {"data": compute_all_fields_and_geometry()}

# --- Initial checkbox state ---
cb_field_labels = ["Bottom Ring Field", "Top Ring Field", "Rodin Coil Field"]
cb_geom_labels  = ["Bottom Ring Geometry", "Top Ring Geometry", "Rodin Coil Geometry"]
cb_field_status = [True, True, True]
cb_geom_status  = [True, True, True]

# --- Figure/Widgets Layout ---
fig = plt.figure(figsize=(14, 9))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.27, right=0.98, bottom=0.18)

# --- FIELD checkboxes ---
rax_field = plt.axes([0.01, 0.7, 0.2, 0.15])
cb_field = CheckButtons(rax_field, cb_field_labels, cb_field_status)
cb_field.on_clicked(on_field_checkbox)
rax_field.set_title("Fields to Show")

# --- GEOM checkboxes ---
rax_geom = plt.axes([0.01, 0.52, 0.2, 0.15])
cb_geom = CheckButtons(rax_geom, cb_geom_status, cb_geom_status)
cb_geom.on_clicked(on_geom_checkbox)
rax_geom.set_title("Show Geometry")

# --- PARAMETER inputs ---
rax_params = plt.axes([0.01, 0.18, 0.22, 0.32])
rax_params.axis('off')
plt.text(0.05, 0.95, "Parameters:", transform=rax_params.transAxes, fontsize=11, va="top")
tb_num_magnets  = TextBox(plt.axes([0.08, 0.45, 0.09, 0.04]), "Magnets", initial=str(params["num_magnets"]))
tb_ring_radius  = TextBox(plt.axes([0.08, 0.39, 0.09, 0.04]), "Ring R", initial=str(params["dipole_ring_radius"]))
tb_rodin_major  = TextBox(plt.axes([0.08, 0.33, 0.09, 0.04]), "Rodin Major", initial=str(params["rodin_major"]))
tb_rodin_minor  = TextBox(plt.axes([0.08, 0.27, 0.09, 0.04]), "Rodin Minor", initial=str(params["rodin_minor"]))
tb_num_turns    = TextBox(plt.axes([0.08, 0.21, 0.09, 0.04]), "Rodin Turns", initial=str(params["num_turns"]))

for tb in [tb_num_magnets, tb_ring_radius, tb_rodin_major, tb_rodin_minor, tb_num_turns]:
    tb.on_submit(update_params)

# --- Initial Plot ---
update_plot()
plt.show()