import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, TextBox, RadioButtons
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')

coil_configs = [
    (40, 11, -9), (34, 11, 7), (30, 11, 3), (32, 13, 9),
    (28, 11, 7), (28, 11, -9), (34, 15, -13), (80, 33, -27),
]
preset_labels = [f"N={c[0]}, +{c[1]}, {c[2]}" for c in coil_configs]

params = {
    "coil_corners": coil_configs[0][0],
    "skip_forward": coil_configs[0][1],
    "skip_backward": coil_configs[0][2],
    "num_layers": 1,
    "layer_spacing": 0.15,
    "grid_dims": (11, 11, 11),
    "x_min": -2.0, "x_max": 2.0,
    "y_min": -2.0, "y_max": 2.0,
    "z_min": -1.0, "z_max": 1.0,
}

def generate_alternating_skip_sequence(corners, step_even, step_odd, radius=1.0, z_layer=0.0, angle_offset=0.0):
    sequence = []
    current = 1
    toggle = True
    for _ in range(corners + 1):
        sequence.append(current)
        step = step_even if toggle else step_odd
        current = (current + step - 1) % corners + 1
        toggle = not toggle
    angles = np.linspace(0, 2*np.pi, corners, endpoint=False) - np.pi/2
    positions = [
        (radius*np.cos(angles[i%corners] + angle_offset),
         radius*np.sin(angles[i%corners] + angle_offset),
         z_layer)
        for i in sequence
    ]
    return {"sequence": sequence, "positions": positions}

def get_wire_arrows(all_positions):
    arrows = []
    for i in range(len(all_positions)-1):
        p0 = np.array(all_positions[i])
        p1 = np.array(all_positions[i+1])
        v = p1-p0
        if v[2] < 0:
            v = -v
        arrows.append((tuple(p0), tuple(v)))
    return arrows

def compute_field_vectors(arrows, grid_dims, x_range, y_range, z_range):
    dl = 0.05
    x = np.linspace(*x_range, grid_dims[0])
    y = np.linspace(*y_range, grid_dims[1])
    z = np.linspace(*z_range, grid_dims[2])
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    Bx = np.zeros_like(X)
    By = np.zeros_like(Y)
    Bz = np.zeros_like(Z)

    for origin, vector in arrows:
        x0, y0, z0 = origin
        dx, dy, dz = vector
        dl_vec = np.array([dx, dy, dz]) * dl
        r0 = np.array([x0, y0, z0])

        RX = X - r0[0]
        RY = Y - r0[1]
        RZ = Z - r0[2]
        norm_R = np.sqrt(RX**2 + RY**2 + RZ**2) + 1e-8

        cross_x = dl_vec[1]*RZ - dl_vec[2]*RY
        cross_y = dl_vec[2]*RX - dl_vec[0]*RZ
        cross_z = dl_vec[0]*RY - dl_vec[1]*RX
        factor = 1 / (norm_R**3)

        Bx += cross_x * factor
        By += cross_y * factor
        Bz += cross_z * factor

    B_mag = np.sqrt(Bx**2 + By**2 + Bz**2) + 1e-9
    return X, Y, Z, Bx / B_mag, By / B_mag, Bz / B_mag, B_mag



def plot_wires(ax, seq, corners, zl, base_color, style='-', alpha=1.0, filter_type='even'):
    angles = np.linspace(0, 2 * np.pi, corners, endpoint=False) - np.pi / 2
    for i in range(len(seq) - 1):
        if (filter_type == "even" and i % 2) or (filter_type == "odd" and i % 2 == 0):
            continue
        a1 = angles[(seq[i] - 1) % corners]
        a2 = angles[(seq[i + 1] - 1) % corners]
        x1, y1 = np.cos(a1), np.sin(a1)
        x2, y2 = np.cos(a2), np.sin(a2)
        z1 = zl + params["layer_spacing"] * (i / (len(seq) - 1))
        z2 = zl + params["layer_spacing"] * ((i + 1) / (len(seq) - 1))
        ax.plot([x1, x2], [y1, y2], [z1, z2], color=base_color, lw=2, linestyle=style, alpha=alpha)


def compute_everything():
    angles = [0, 2*np.pi/3, 4*np.pi/3]
    colors = ['#00ccff', '#33ff66', '#ff3366']
    phases=[]
    for a in angles:
        sd = generate_alternating_skip_sequence(params["coil_corners"],
                                                params["skip_forward"], params["skip_backward"],
                                                angle_offset=a)
        pos=[]
        for L in range(params["num_layers"]):
            off = L*params["layer_spacing"]
            pos += [(x,y,z+off) for x,y,z in sd["positions"]]
        phases.append((sd["sequence"], pos))
    arrows = get_wire_arrows(phases[0][1])
    X,Y,Z,Bx,By,Bz,mag = compute_field_vectors(arrows, params["grid_dims"],
                                               (params["x_min"],params["x_max"]),(params["y_min"],params["y_max"]),(params["z_min"],params["z_max"]))
    return {"phases": phases, "colors": colors, "X":X,"Y":Y,"Z":Z,"Bx":Bx,"By":By,"Bz":Bz,"mag":mag}

def update_plot(*args):
    show_field = cb_status[0]
    show_even = cb_status[1]
    show_odd = cb_status[2]
    by_dir = cb_status[3]
    by_layer = cb_status[4]
    by_mag = cb_status[5]

    data = gui_state["data"]
    ax.clear()
    ax.set_facecolor(fig.get_facecolor())

    if show_field:
        X, Y, Z = data["X"], data["Y"], data["Z"]
        Bx, By, Bz = data["Bx"], data["By"], data["Bz"]
        mag = np.sqrt(Bx**2 + By**2 + Bz**2)

        density = 2
        Xf, Yf, Zf = X[::density,::density,::density], Y[::density,::density,::density], Z[::density,::density,::density]
        Bxf, Byf, Bzf = Bx[::density,::density,::density], By[::density,::density,::density], Bz[::density,::density,::density]
        magf = mag[::density,::density,::density]

        Xf, Yf, Zf = Xf.flatten(), Yf.flatten(), Zf.flatten()
        Bxf, Byf, Bzf = Bxf.flatten(), Byf.flatten(), Bzf.flatten()
        magf = magf.flatten()

        if by_mag:
            lengths = 0.07 * (magf / (np.max(magf) + 1e-8))
            gray_vals = (magf - np.min(magf)) / np.ptp(magf)
            colors = np.stack([gray_vals*0.9]*3 + [np.ones_like(gray_vals)], axis=1)
        elif by_dir:
            zn = (Bzf - np.min(Bzf)) / np.ptp(Bzf)
            colors = plt.cm.coolwarm(zn)
            lengths = np.full_like(zn, 0.07)
        elif by_layer:
            zl = (Zf - np.min(Zf)) / np.ptp(Zf)
            colors = plt.cm.plasma(zl)
            lengths = np.full_like(zl, 0.07)
        else:
            colors = 'teal'
            lengths = np.full_like(magf, 0.07)

        if isinstance(colors, str):
            ax.quiver(Xf, Yf, Zf, Bxf, Byf, Bzf, length=0.07, normalize=True,
                      color=colors, linewidth=0.5, arrow_length_ratio=0.3)
        else:
            for xi, yi, zi, dxi, dyi, dzi, ci, li in zip(Xf, Yf, Zf, Bxf, Byf, Bzf, colors, lengths):
                ax.quiver(xi, yi, zi, dxi, dyi, dzi, length=li, normalize=False,
                          color=ci, linewidth=0.5, arrow_length_ratio=0.3)

    for (seq, _), color in zip(data["phases"], data["colors"]):
        for layer in range(params["num_layers"]):
            z_layer = layer * params["layer_spacing"]
            if show_even:
                plot_wires(ax, seq, params["coil_corners"], z_layer, '#aa6600', '-', alpha=1.0, filter_type='even')
            if show_odd:
                plot_wires(ax, seq, params["coil_corners"], z_layer, '#880000', '-', alpha=1.0, filter_type='odd')

    ax.set_title(f"3-Phase Coil: N={params['coil_corners']} Skip=({params['skip_forward']}, {params['skip_backward']})", color='white')
    ax.set_xlim(params["x_min"], params["x_max"])
    ax.set_ylim(params["y_min"], params["y_max"])
    ax.set_zlim(params["z_min"], params["z_max"])
    ax.set_axis_off()
    ax.view_init(elev=88, azim=45)
    fig.canvas.draw_idle()


def on_checkbox(label):
    idx=cb_labels.index(label); cb_status[idx] = not cb_status[idx]; update_plot()

def on_param_submit(label):
    try:
        corners = int(tb_corners.text)
        layers = int(tb_layers.text)
        skip_fwd = int(tb_skip_fwd.text)
        skip_bwd = int(tb_skip_bwd.text)
        spacing = float(tb_spacing.text)
        grid_x = int(tb_xres.text)
        grid_y = int(tb_yres.text)
        grid_z = int(tb_zres.text)
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
    params["grid_dims"] = (grid_x, grid_y, grid_z)
    params["x_min"], params["x_max"] = x_min, x_max
    params["y_min"], params["y_max"] = y_min, y_max
    params["z_min"], params["z_max"] = z_min, z_max
    gui_state["data"] = compute_everything()
    update_plot()

def on_preset(label):
    i=preset_labels.index(label)
    c,f,b = coil_configs[i]
    tb_corners.set_val(str(c)); tb_skip_fwd.set_val(str(f)); tb_skip_bwd.set_val(str(b))
    on_param_submit(label)

gui_state = {"data": compute_everything()}
cb_labels = ["Field Arrows","Even Segments","Odd Segments","Color Dir","Color Layer","Color Mag"]
cb_status = [True,True,True,False,False,False]

fig = plt.figure(figsize=(14,10))
ax = fig.add_subplot(111,projection='3d')
plt.subplots_adjust(left=0.36, right=0.98, bottom=0.28, top=0.98)


# Replace color checkboxes with RadioButtons
rax_color = plt.axes([0.01, 0.82, 0.18, 0.12])
color_modes = ["Default", "By Direction", "By Layer", "By Magnitude"]
rb_color = RadioButtons(rax_color, color_modes, active=0)
def on_color_mode(label):
    # Reset color flags
    cb_status[3:] = [label == m for m in color_modes[1:]]
    update_plot()
rb_color.on_clicked(on_color_mode)
rax_color.set_title("Color Mode")


rax_preset = plt.axes([0.01, 0.66, 0.30, 0.15])
rb = RadioButtons(rax_preset, preset_labels)
rax_preset.set_title("Presets")
rb.on_clicked(on_preset)

plt.axes([0.01,0.30,0.33,0.10]).axis('off')
tb_corners = TextBox(plt.axes([0.13,0.38,0.09,0.04]), "Corners", initial=str(params["coil_corners"]))
tb_layers = TextBox(plt.axes([0.13,0.33,0.09,0.04]), "Layers", initial=str(params["num_layers"]))
tb_skip_fwd = TextBox(plt.axes([0.13,0.28,0.09,0.04]), "Skip Fwd", initial=str(params["skip_forward"]))
tb_skip_bwd = TextBox(plt.axes([0.13,0.23,0.09,0.04]), "Skip Bwd", initial=str(params["skip_backward"]))
tb_spacing = TextBox(plt.axes([0.13,0.18,0.09,0.04]), "Spacing", initial=str(params["layer_spacing"]))
tb_grid = TextBox(plt.axes([0.13,0.13,0.09,0.04]), "Grid N", initial=str(params["grid_dims"]))

tb_xmin = TextBox(plt.axes([0.25,0.38,0.07,0.04]), "Xmin", initial=str(params["x_min"]))
tb_xmax = TextBox(plt.axes([0.25,0.33,0.07,0.04]), "Xmax", initial=str(params["x_max"]))
tb_ymin = TextBox(plt.axes([0.25,0.28,0.07,0.04]), "Ymin", initial=str(params["y_min"]))
tb_ymax = TextBox(plt.axes([0.25,0.23,0.07,0.04]), "Ymax", initial=str(params["y_max"]))
tb_zmin = TextBox(plt.axes([0.25,0.18,0.07,0.04]), "Zmin", initial=str(params["z_min"]))
tb_zmax = TextBox(plt.axes([0.25,0.13,0.07,0.04]), "Zmax", initial=str(params["z_max"]))
tb_xres = TextBox(plt.axes([0.13, 0.08, 0.09, 0.04]), "X res", initial=str(params["grid_dims"][0]))
tb_yres = TextBox(plt.axes([0.13, 0.03, 0.09, 0.04]), "Y res", initial=str(params["grid_dims"][1]))
tb_zres = TextBox(plt.axes([0.25, 0.08, 0.07, 0.04]), "Z res", initial=str(params["grid_dims"][2]))

from matplotlib.widgets import Slider

# XY resolution slider
ax_sl_xy = plt.axes([0.05, 0.5, 0.25, 0.03])
slider_xy = Slider(ax_sl_xy, 'Grid XY', 2, 50, valinit=params["grid_dims"][0], valstep=1)

# Z resolution slider
ax_sl_z = plt.axes([0.05, 0.45, 0.25, 0.03])
slider_z = Slider(ax_sl_z, 'Grid Z', 1, 20, valinit=params["grid_dims"][2], valstep=1)

def on_slider_change(val):
    params["grid_dims"] = (int(slider_xy.val), int(slider_xy.val), int(slider_z.val))
    gui_state["data"] = compute_everything()
    update_plot()

slider_xy.on_changed(on_slider_change)
slider_z.on_changed(on_slider_change)


for tb in [tb_corners, tb_layers, tb_skip_fwd, tb_skip_bwd, tb_spacing,
           tb_xres, tb_yres, tb_zres,
           tb_xmin, tb_xmax, tb_ymin, tb_ymax, tb_zmin, tb_zmax]:
    tb.on_submit(on_param_submit)

update_plot()
plt.show()