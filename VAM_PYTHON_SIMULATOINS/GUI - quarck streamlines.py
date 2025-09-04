import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.widgets import Button, Slider, CheckButtons
import matplotlib
matplotlib.use('TkAgg')

L = 8.0
N = 300
x = np.linspace(-L, L, N)
y = np.linspace(-L, L, N)
X, Y = np.meshgrid(x, y)

def triangle_positions(a, center):
    cx, cy = center
    return [
        (cx + a, cy),
        (cx - a/2, cy + a*np.sqrt(3)/2),
        (cx - a/2, cy - a*np.sqrt(3)/2)
    ]

def quark_circle_radius(a): return a
def proton_group_radius(a): return 2 * a

class Proton:
    def __init__(self, center, triangle_a, polarity, color, show_quarks=True):
        self.center = np.array(center)
        self.triangle_a = triangle_a
        self.polarity = list(polarity)
        self.color = color
        self.show_quarks = show_quarks
        self.patch = None
        self.quark_patches = []
        self.remove_patch = None

def vortex_field(x0, y0, gamma, sigma=0.045):
    dx = X - x0
    dy = Y - y0
    r2 = dx**2 + dy**2
    factor = gamma / (2 * np.pi * r2) * (1 - np.exp(-r2 / (2 * sigma**2)))
    u = -dy * factor
    v = dx * factor
    return u, v

class ProtonManager:
    def __init__(self):
        self.protons = [
            Proton(center=(0,0), triangle_a=0.45, polarity=[1,1,1], color='royalblue')
        ]
        self.dragged = None
        self.drag_offset = (0,0)
        self.hover_idx = None
        # global field-wide settings:
        self.sigma = 0.045
        self.gamma_base = 5
        self.spacing = 4.5
        self.triangle_a = 0.45
        self.stream_density = 2.2
        self.show_quarks = True

    def compute_fields(self):
        U = np.zeros_like(X)
        V = np.zeros_like(Y)
        for p in self.protons:
            positions = triangle_positions(p.triangle_a, p.center)
            for (x0, y0), sign in zip(positions, p.polarity):
                u, v = vortex_field(x0, y0, self.gamma_base*sign, sigma=self.sigma)
                U += u
                V += v
        return U, V

    def find_proton(self, mouseevent):
        xy = np.array([mouseevent.xdata, mouseevent.ydata])
        dists = [np.linalg.norm(p.center-xy) for p in self.protons]
        if not dists or any(np.isnan(dists)): return None, None
        idx = np.argmin(dists)
        if dists[idx] < proton_group_radius(self.protons[idx].triangle_a) * 1.1:
            return idx, dists[idx]
        return None, None

    def find_remove(self, mouseevent):
        for idx, p in enumerate(self.protons):
            if p.remove_patch is not None:
                bbox = p.remove_patch.get_window_extent()
                if bbox.contains(mouseevent.x, mouseevent.y):
                    return idx
        return None

    def update_protons_from_controls(self):
        for p in self.protons:
            p.triangle_a = self.triangle_a
            p.show_quarks = self.show_quarks

pm = ProtonManager()

fig, ax = plt.subplots(figsize=(13,13))
plt.subplots_adjust(left=0.26, right=0.98, top=0.98, bottom=0.17)

def update_plot(event=None):
    pm.update_protons_from_controls()
    U, V = pm.compute_fields()
    ax.clear()
    ax.streamplot(x, y, U, V, color='k', density=pm.stream_density, linewidth=1.2)
    for idx, p in enumerate(pm.protons):
        group_R = proton_group_radius(p.triangle_a)
        p.patch = Circle(p.center, group_R, color=p.color, fill=False, lw=2.5, alpha=0.42, zorder=1)
        ax.add_patch(p.patch)
        if pm.show_quarks and p.show_quarks:
            pos = triangle_positions(p.triangle_a, p.center)
            p.quark_patches = []
            for (qx, qy) in pos:
                qc = Circle((qx, qy), quark_circle_radius(p.triangle_a),
                            color='red', fill=True, alpha=0.72, lw=1.6, zorder=2, ec='black')
                ax.add_patch(qc)
                ax.plot(qx, qy, marker='o', markersize=11, color='black', zorder=3,
                        markeredgecolor='white', markeredgewidth=1.5)
                ax.plot(qx, qy, marker='o', markersize=6, color='red', zorder=4,
                        markeredgecolor='black', markeredgewidth=0.9)
                p.quark_patches.append(qc)
        if pm.hover_idx == idx:
            theta = np.deg2rad(65)
            rx, ry = p.center[0] + group_R*np.cos(theta), p.center[1] + group_R*np.sin(theta)
            p.remove_patch = ax.annotate(
                "-", xy=(rx, ry), ha='center', va='center',
                fontsize=23, color='darkred', fontweight='bold',
                bbox=dict(boxstyle='circle,pad=0.17', fc='white', ec='red', lw=1.5, alpha=0.86),
                zorder=10)
        else:
            p.remove_patch = None
    ax.set_xlim(-L, L)
    ax.set_ylim(-L, L)
    ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Drag protons, hover to remove (-), add more below", fontsize=16)
    fig.canvas.draw_idle()

def on_press(event):
    if event.inaxes != ax: return
    idx = pm.find_remove(event)
    if idx is not None:
        pm.protons.pop(idx)
        pm.hover_idx = None
        update_plot()
        return
    idx, dist = pm.find_proton(event)
    if idx is not None:
        pm.dragged = idx
        pm.drag_offset = pm.protons[idx].center - np.array([event.xdata, event.ydata])

def on_release(event):
    pm.dragged = None

def on_motion(event):
    changed = False
    idx, _ = pm.find_proton(event) if (event.inaxes == ax and event.xdata is not None) else (None, None)
    if idx != pm.hover_idx:
        pm.hover_idx = idx
        changed = True
    if pm.dragged is not None and event.inaxes == ax and event.xdata is not None:
        center = np.array([event.xdata, event.ydata]) + pm.drag_offset
        pm.protons[pm.dragged].center = center
        changed = True
    if changed:
        update_plot()

def add_proton(event):
    angle = np.random.uniform(0, 2*np.pi)
    rad = np.random.uniform(L*0.2, L*0.8)
    x0, y0 = rad*np.cos(angle), rad*np.sin(angle)
    pm.protons.append(Proton(center=(x0,y0),
                             triangle_a=pm.triangle_a, polarity=[1,1,1], color='royalblue', show_quarks=pm.show_quarks))
    update_plot()

def add_antiproton(event):
    angle = np.random.uniform(0, 2*np.pi)
    rad = np.random.uniform(L*0.2, L*0.8)
    x0, y0 = rad*np.cos(angle), rad*np.sin(angle)
    pm.protons.append(Proton(center=(x0,y0),
                             triangle_a=pm.triangle_a, polarity=[-1,-1,-1], color='green', show_quarks=pm.show_quarks))
    update_plot()

def on_spacing_slider(val):
    pm.spacing = spacing_slider.val
    update_plot()

def on_triangle_slider(val):
    pm.triangle_a = triangle_slider.val
    update_plot()

def on_density_slider(val):
    pm.stream_density = density_slider.val
    update_plot()

def cb_quark_handler(label):
    pm.show_quarks = not pm.show_quarks
    update_plot()

# --- Controls ---
rax_spacing = plt.axes([0.03, 0.88, 0.18, 0.045])
spacing_slider = Slider(rax_spacing, "Grid Spacing", 1.2, 7.5, valinit=pm.spacing, valstep=0.01)
spacing_slider.on_changed(on_spacing_slider)

rax_triangle = plt.axes([0.03, 0.82, 0.18, 0.045])
triangle_slider = Slider(rax_triangle, "Quark Distance", 0.045, 1, valinit=pm.triangle_a, valstep=0.001)
triangle_slider.on_changed(on_triangle_slider)

rax_density = plt.axes([0.03, 0.76, 0.18, 0.045])
density_slider = Slider(rax_density, "Stream Density", 0.6, 4.7, valinit=pm.stream_density, valstep=0.01)
density_slider.on_changed(on_density_slider)

rax_quark = plt.axes([0.03, 0.70, 0.18, 0.045])
cb_quark = CheckButtons(rax_quark, ["Show Quarks"], [pm.show_quarks])
cb_quark.on_clicked(cb_quark_handler)

# --- Add buttons for Proton / Anti-Proton ---
rax_add = plt.axes([0.34, 0.045, 0.15, 0.065])
btn_add = Button(rax_add, "Add Proton", color='#d7f0fa', hovercolor='#abd9ea')
btn_add.on_clicked(add_proton)
rax_anti = plt.axes([0.52, 0.045, 0.15, 0.065])
btn_anti = Button(rax_anti, "Add Anti-Proton", color='#fadada', hovercolor='#ffc6c6')
btn_anti.on_clicked(add_antiproton)

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

fig.text(0.042, 0.62,
         "• Drag & drop protons, hover for delete (-)\n"
         "• Add protons (blue) or anti-protons (green)\n"
         "• All new inherit current triangle & quark settings\n"
         "• Sliders: grid spacing, triangle size, stream density\n"
         "• Checkbox: hide/show all quarks\n",
         fontsize=11, color='gray')

update_plot()
plt.show()