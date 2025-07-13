import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, TextBox
import os
import matplotlib
matplotlib.use('TkAgg')

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
    z = r * np.sin(phi) * 0.3
    return x, y, z

# --- Biot-Savart for wire loop (numerical) ---
def biot_savart_wire(X, Y, Z, wire_points, current=1.0):
    mu0 = 1.0
    dBx = np.zeros_like(X)
    dBy = np.zeros_like(Y)
    dBz = np.zeros_like(Z)
    N = wire_points.shape[0]
    dl = np.diff(wire_points, axis=0)
    r_mid = 0.5 * (wire_points[:-1] + wire_points[1:])  # segment midpoints
    for idx in range(N-1):
        Rx = X - r_mid[idx,0]
        Ry = Y - r_mid[idx,1]
        Rz = Z - r_mid[idx,2]
        R = np.stack([Rx, Ry, Rz], axis=-1)
        normR = np.linalg.norm(R, axis=-1)
        mask = normR > 1e-7
        dl_cross_R = np.cross(dl[idx], R)
        factor = (mu0 * current) / (4 * np.pi)
        contrib = factor * dl_cross_R / (normR[...,None]**3)
        dBx[mask] += contrib[mask,0]
        dBy[mask] += contrib[mask,1]
        dBz[mask] += contrib[mask,2]
    return dBx, dBy, dBz

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

def magnetic_field_dipole(r, m):
    mu0 = 1.0
    norm_r = np.linalg.norm(r)
    if norm_r < 1e-8:
        return np.zeros(3)
    r_hat = r / norm_r
    return (mu0 / (4 * np.pi * norm_r**3)) * (3 * np.dot(m, r_hat) * r_hat - m)

def compute_dipole_field_from_orientations(X, Y, Z, positions, orientations):
    Bx, By, Bz = np.zeros_like(X), np.zeros_like(Y), np.zeros_like(Z)
    for pos, m in zip(positions, orientations):
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                for k in range(X.shape[2]):
                    r = np.array([X[i, j, k], Y[i, j, k], Z[i, j, k]]) - pos
                    B = magnetic_field_dipole(r, m)
                    Bx[i, j, k] += B[0]
                    By[i, j, k] += B[1]
                    Bz[i, j, k] += B[2]
    return Bx, By, Bz

# --- Initial Parameters (user can edit) ---
params = {
    "num_magnets": 16,
    "dipole_ring_radius": 1.5,
    "rodin_major": 1.2,
    "rodin_minor": 0.6,
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
    # Update all geometry and fields as per current params
    bottom_pos, bottom_ori = generate_dipole_ring(params["dipole_ring_radius"], params["num_magnets"], z_offset=z_offset_bottom, invert=False)
    top_pos, top_ori = generate_dipole_ring(params["dipole_ring_radius"], params["num_magnets"], z_offset=z_offset_top, invert=True)
    winding_colors = np.linspace(0, 1, params["num_magnets"], endpoint=False)
    rodin_x, rodin_y, rodin_z = generate_rodin_starship(
        R=params["rodin_major"], r=params["rodin_minor"], num_turns=params["num_turns"], num_points=num_points)
    rodin_wire_points = np.stack([rodin_x, rodin_y, rodin_z], axis=-1)
    X, Y, Z = np.meshgrid(
        np.linspace(*x_range, field_grid_N),
        np.linspace(*y_range, field_grid_N),
        np.linspace(*z_range, field_grid_N)
    )
    print("Recomputing all fields for new parameters...")
    Bx_bottom, By_bottom, Bz_bottom = compute_dipole_field_from_orientations(
        X, Y, Z, bottom_pos, bottom_ori)
    Bx_top, By_top, Bz_top = compute_dipole_field_from_orientations(
        X, Y, Z, top_pos, top_ori)
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

    # SAFELY initialize arrays!
    Bx = np.zeros_like(Bx_bottom)
    By = np.zeros_like(By_bottom)
    Bz = np.zeros_like(Bz_bottom)

    field_components = []
    if show_bottom_field:
        Bx += Bx_bottom
        By += By_bottom
        Bz += Bz_bottom
        field_components.append("Bottom Ring")
    if show_top_field:
        Bx += Bx_top
        By += By_top
        Bz += Bz_top
        field_components.append("Top Ring")
    if show_rodin_field:
        Bx += Bx_rodin
        By += By_rodin
        Bz += Bz_rodin
        field_components.append("Rodin Coil")

    Bmag = np.sqrt(Bx**2 + By**2 + Bz**2)
    Bmag[Bmag == 0] = 1e-9
    Bx_norm = Bx / Bmag
    By_norm = By / Bmag
    Bz_norm = Bz / Bmag

    ax.clear()
    if show_bottom_field or show_top_field or show_rodin_field:
        ax.quiver(
            X, Y, Z, Bx_norm, By_norm, Bz_norm,
            length=0.15, normalize=True, color='blue', linewidth=0.5, alpha=0.9
        )

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
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(*x_range)
    ax.set_ylim(*y_range)
    ax.set_zlim(*z_range)
    ax.set_box_aspect([1, 1, 1])
    try:
        ax.legend()
    except Exception:
        pass
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
cb_geom = CheckButtons(rax_geom, cb_geom_labels, cb_geom_status)
cb_geom.on_clicked(on_geom_checkbox)
rax_geom.set_title("Show Geometry")

# --- PARAMETER inputs ---
# Add TextBoxes for parameter input
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
