import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, TextBox, RadioButtons
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')

# Preset coil configurations
coil_configs = [
    (32, 11, -9),
    (34, 11,  7),
    (30, 11,  3),
    (32, 13,  9),
    (28, 11,  7),
    (28, 11, -9),
    (34, 15, -13),
    (80, 33, -27),
]
preset_labels = [f"N={c[0]}, +{c[1]}, {c[2]}" for c in coil_configs]

params = {
    "coil_corners": coil_configs[0][0],
    "skip_forward": coil_configs[0][1],
    "skip_backward": coil_configs[0][2],
    "num_layers": 5,
    "layer_spacing": 0.15,
    "grid_size": 11,
    "x_min": -1.0, "x_max": 1.0,
    "y_min": -1.0, "y_max": 1.0,
    "z_min":  0.0, "z_max": 1.0,
}

def generate_alternating_skip_sequence(corners, step_even, step_odd, radius=1.0, z_layer=0.0):
    sequence = []
    current = 1
    toggle = True
    for _ in range(corners + 1):
        sequence.append(current)
        step = step_even if toggle else step_odd
        current = (current + step - 1) % corners + 1
        toggle = not toggle
    angles = np.linspace(0, 2 * np.pi, corners, endpoint=False) - np.pi / 2
    positions = [(radius * np.cos(angles[(i - 1) % corners]),
                  radius * np.sin(angles[(i - 1) % corners]),
                  z_layer) for i in sequence]
    even_steps = [(sequence[i], sequence[i+1]) for i in range(0, len(sequence)-1, 2)]
    odd_steps = [(sequence[i], sequence[i+1]) for i in range(1, len(sequence)-1, 2)]
    return {
        "sequence": sequence,
        "even_pairs": even_steps,
        "odd_pairs": odd_steps,
        "positions": positions
    }

def get_wire_arrows(all_positions):
    arrows = []
    for i in range(len(all_positions) - 1):
        x0, y0, z0 = all_positions[i]
        x1, y1, z1 = all_positions[i + 1]
        dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
        arrows.append(((x0, y0, z0), (dx, dy, dz)))
    return arrows

def compute_field_vectors(arrows, grid_size, x_range, y_range, z_range):
    dl = 0.05
    x = np.linspace(*x_range, grid_size)
    y = np.linspace(*y_range, grid_size)
    z = np.linspace(*z_range, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    Bx = np.zeros_like(X)
    By = np.zeros_like(Y)
    Bz = np.zeros_like(Z)
    for origin, vector in arrows:
        x0, y0, z0 = origin
        dx, dy, dz = vector
        segment = np.array([dx, dy, dz]) * dl
        r0 = np.array([x0, y0, z0])
        for i in range(grid_size):
            for j in range(grid_size):
                for k in range(grid_size):
                    r = np.array([X[i, j, k], Y[i, j, k], Z[i, j, k]])
                    R = r - r0
                    norm_R = np.linalg.norm(R)
                    if norm_R < 1e-3:
                        continue
                    dB = np.cross(segment, R) / (norm_R**3)
                    Bx[i, j, k] += dB[0]
                    By[i, j, k] += dB[1]
                    Bz[i, j, k] += dB[2]
    B_magnitude = np.sqrt(Bx**2 + By**2 + Bz**2)
    Bx /= (B_magnitude + 1e-9)
    By /= (B_magnitude + 1e-9)
    Bz /= (B_magnitude + 1e-9)
    return X, Y, Z, Bx, By, Bz

def plot_wires(ax, sequence, coil_corners, z_layer, base_color, style, alpha=1.0, filter_type='even'):
    angles = np.linspace(0, 2 * np.pi, coil_corners, endpoint=False) - np.pi / 2
    total_points = len(sequence) - 1
    for i in range(total_points):
        if (filter_type == 'even' and i % 2 != 0) or (filter_type == 'odd' and i % 2 == 0):
            continue
        angle_start = angles[(sequence[i] - 1) % coil_corners]
        angle_end = angles[(sequence[i + 1] - 1) % coil_corners]
        x_start, y_start = np.cos(angle_start), np.sin(angle_start)
        x_end, y_end = np.cos(angle_end), np.sin(angle_end)
        z_start = z_layer + params["layer_spacing"] * (i / total_points)
        z_end = z_layer + params["layer_spacing"] * ((i + 1) / total_points)
        ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end],
                color=base_color, linestyle=style, linewidth=2, alpha=alpha)

def compute_everything():
    sequence_data = generate_alternating_skip_sequence(
        params["coil_corners"], params["skip_forward"], params["skip_backward"])
    sequence = sequence_data["sequence"]
    all_positions = []
    for layer in range(params["num_layers"]):
        z_offset = layer * params["layer_spacing"]
        for (x, y, z) in sequence_data["positions"]:
            all_positions.append((x, y, z + z_offset))
    arrows = get_wire_arrows(all_positions)
    X, Y, Z, Bx, By, Bz = compute_field_vectors(
        arrows, params["grid_size"],
        (params["x_min"], params["x_max"]),
        (params["y_min"], params["y_max"]),
        (params["z_min"], params["z_max"])
    )
    return {
        "sequence_data": sequence_data,
        "arrows": arrows,
        "all_positions": all_positions,
        "X": X, "Y": Y, "Z": Z,
        "Bx": Bx, "By": By, "Bz": Bz
    }

def update_plot(*args):
    show_field = cb_status[0]
    show_even = cb_status[1]
    show_odd = cb_status[2]
    data = gui_state["data"]
    ax.clear()
    if show_field:
        ax.quiver(data["X"], data["Y"], data["Z"], data["Bx"], data["By"], data["Bz"],
                  length=0.07, normalize=True, color='cyan', alpha=0.7)
    seq = data["sequence_data"]["sequence"]
    for layer in range(params["num_layers"]):
        z_layer = layer * params["layer_spacing"]
        if show_even:
            plot_wires(ax, seq, params["coil_corners"], z_layer, '#ff9900', '-', alpha=1.0, filter_type='even')
        if show_odd:
            plot_wires(ax, seq, params["coil_corners"], z_layer, '#cc0000', '-', alpha=1.0, filter_type='odd')
    ax.set_title(f"Starship Coil: N={params['coil_corners']} Skip=({params['skip_forward']}, {params['skip_backward']})", color='white')
    ax.set_xlim(params["x_min"], params["x_max"])
    ax.set_ylim(params["y_min"], params["y_max"])
    ax.set_zlim(params["z_min"], params["z_max"])
    ax.set_axis_off()
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.view_init(elev=88, azim=45)
    fig.canvas.draw_idle()

def on_checkbox(label):
    idx = cb_labels.index(label)
    cb_status[idx] = not cb_status[idx]
    update_plot()

def on_param_submit(label):
    try:
        corners = int(tb_corners.text)
        layers = int(tb_layers.text)
        skip_fwd = int(tb_skip_fwd.text)
        skip_bwd = int(tb_skip_bwd.text)
        spacing = float(tb_spacing.text)
        grid = int(tb_grid.text)
        x_min = float(tb_xmin.text)
        x_max = float(tb_xmax.text)
        y_min = float(tb_ymin.text)
        y_max = float(tb_ymax.text)
        z_min = float(tb_zmin.text)
        z_max = float(tb_zmax.text)
        assert corners > 2 and layers > 0
    except Exception as e:
        print("Invalid input:", e)
        return
    params["coil_corners"] = corners
    params["skip_forward"] = skip_fwd
    params["skip_backward"] = skip_bwd
    params["num_layers"] = layers
    params["layer_spacing"] = spacing
    params["grid_size"] = grid
    params["x_min"], params["x_max"] = x_min, x_max
    params["y_min"], params["y_max"] = y_min, y_max
    params["z_min"], params["z_max"] = z_min, z_max
    gui_state["data"] = compute_everything()
    update_plot()

def on_preset(label):
    idx = preset_labels.index(label)
    corners, skip_fwd, skip_bwd = coil_configs[idx]
    # update parameter textboxes
    tb_corners.set_val(str(corners))
    tb_skip_fwd.set_val(str(skip_fwd))
    tb_skip_bwd.set_val(str(skip_bwd))
    # All parameters update!
    on_param_submit(label)

gui_state = {"data": compute_everything()}
cb_labels = ["Field Arrows", "Even Segments", "Odd Segments"]
cb_status = [True, True, True]

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(left=0.34, right=0.98, bottom=0.28)

rax_cb = plt.axes([0.01, 0.68, 0.17, 0.15])
cb = CheckButtons(rax_cb, cb_labels, cb_status)
cb.on_clicked(on_checkbox)
rax_cb.set_title("Show")

# --- NEW: Preset selector ---
rax_preset = plt.axes([0.01, 0.55, 0.30, 0.12])
rb = RadioButtons(rax_preset, preset_labels)
rax_preset.set_title("Presets")
rb.on_clicked(on_preset)

# PARAM INPUTS: with range controls!
plt.axes([0.01, 0.30, 0.33, 0.25]).axis('off')
tb_corners  = TextBox(plt.axes([0.13, 0.65, 0.09, 0.04]), "Corners", initial=str(params["coil_corners"]))
tb_layers   = TextBox(plt.axes([0.13, 0.60, 0.09, 0.04]), "Layers", initial=str(params["num_layers"]))
tb_skip_fwd = TextBox(plt.axes([0.13, 0.55, 0.09, 0.04]), "Skip Fwd", initial=str(params["skip_forward"]))
tb_skip_bwd = TextBox(plt.axes([0.13, 0.50, 0.09, 0.04]), "Skip Bwd", initial=str(params["skip_backward"]))
tb_spacing  = TextBox(plt.axes([0.13, 0.45, 0.09, 0.04]), "Spacing", initial=str(params["layer_spacing"]))
tb_grid     = TextBox(plt.axes([0.13, 0.40, 0.09, 0.04]), "Grid N", initial=str(params["grid_size"]))

tb_xmin = TextBox(plt.axes([0.25, 0.65, 0.07, 0.04]), "Xmin", initial=str(params["x_min"]))
tb_xmax = TextBox(plt.axes([0.25, 0.60, 0.07, 0.04]), "Xmax", initial=str(params["x_max"]))
tb_ymin = TextBox(plt.axes([0.25, 0.55, 0.07, 0.04]), "Ymin", initial=str(params["y_min"]))
tb_ymax = TextBox(plt.axes([0.25, 0.50, 0.07, 0.04]), "Ymax", initial=str(params["y_max"]))
tb_zmin = TextBox(plt.axes([0.25, 0.45, 0.07, 0.04]), "Zmin", initial=str(params["z_min"]))
tb_zmax = TextBox(plt.axes([0.25, 0.40, 0.07, 0.04]), "Zmax", initial=str(params["z_max"]))

for tb in [tb_corners, tb_layers, tb_skip_fwd, tb_skip_bwd, tb_spacing, tb_grid,
           tb_xmin, tb_xmax, tb_ymin, tb_ymax, tb_zmin, tb_zmax]:
    tb.on_submit(on_param_submit)

update_plot()
plt.show()
