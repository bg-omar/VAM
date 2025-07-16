import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]


# Trefoil 2D projection
t = np.linspace(0, 2 * np.pi, 2000)
x = np.sin(t) + 2 * np.sin(2 * t)
y = np.cos(t) - 2 * np.cos(2 * t)

# Define crossing t-intervals
crossings = [
    (1.8, 1.85),
    (3.9, 3.95),
    (5.99, 6.04),
]

fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(x, y, linewidth=4, color='darkblue', zorder=1)

# Mask the underpasses
for t_start, t_end in crossings:
    idx = (t >= t_start) & (t <= t_end)
    ax.plot(x[idx], y[idx], color='white', linewidth=16, zorder=2)

# Redraw overpasses *after* masking
for t_start, t_end in crossings:
    idx = (t >= t_start-0.5) & (t <= t_end+0.5)
    ax.plot(x[idx], y[idx], color='darkblue', linewidth=4, zorder=3)

# Style
ax.axis('equal')
ax.axis('off')
ax.set_title("Trefoil Knot T(3,2)", fontsize=12)
plt.savefig("trefoil_knot_3.2.png", dpi=300, bbox_inches='tight')

x= -x
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(x, y, linewidth=4, color='darkblue', zorder=1)

# Mask the underpasses
for t_start, t_end in crossings:
    idx = (t >= t_start) & (t <= t_end)
    ax.plot(x[idx], y[idx], color='white', linewidth=16, zorder=2)

# Redraw overpasses *after* masking
for t_start, t_end in crossings:
    idx = (t >= t_start-0.5) & (t <= t_end+0.5)
    ax.plot(x[idx], y[idx], color='darkblue', linewidth=4, zorder=3)

# Style
ax.axis('equal')
ax.axis('off')
ax.set_title("Trefoil Knot T(2,3)", fontsize=12)
plt.savefig("trefoil_knot_2.3.png", dpi=300, bbox_inches='tight')


# Generate and plot figure-eight knot approximation via Lissajous-like form (not a torus knot)
t_figure8 = np.linspace(0, 2 * np.pi, 4000)
x_figure8 = (2 + np.cos(2 * t_figure8)) * np.cos(3 * t_figure8)
y_figure8 = (2 + np.cos(2 * t_figure8)) * np.sin(3 * t_figure8)
crossings_fig8 = [(0.4, 0.45), (1.5, 1.55), (4.8, 4.85), (5.5, 5.55)]

# Regenerate the plots with corrected overpass intervals and show explicitly

def plot_knot_with_crossings_fixed(x, y, t, crossings, filename="knot.png", title="Knot"):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x, y, linewidth=4, color='darkblue', zorder=1)

    for t_start, t_end in crossings:
        idx = (t >= t_start) & (t <= t_end)
        ax.plot(x[idx], y[idx], color='white', linewidth=16, zorder=2)

    for t_start, t_end in crossings:
        idx = (t >= t_start - 0.5) & (t <= t_end + 0.5)  # narrower slice centered within white mask
        ax.plot(x[idx], y[idx], color='darkblue', linewidth=4, zorder=3)

    ax.axis('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=12)
    plt.savefig(f"{filename}", dpi=300, bbox_inches='tight')



# Replot Figure-Eight approximation
plot_knot_with_crossings_fixed(x_figure8, y_figure8, t_figure8, crossings_fig8, "figure8_knot_fixed.png", "Figure-Eight Approximation")


# Re-import libraries after code execution state reset
import numpy as np
import matplotlib.pyplot as plt

def plot_knot(x, y, title="Knot", filename="knot.png"):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x, y, color='darkblue', linewidth=4)
    ax.axis('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=12)
    plt.savefig(f"{filename}", dpi=300, bbox_inches='tight')
    plt.close()

# Precomputed 2D approximations (not exact parameterizations) of 6_2 and 7_4 knots
t = np.linspace(0, 2 * np.pi, 2000)

# Approximation for knot 6_2
x_62 = np.sin(3 * t) + 0.5 * np.sin(6 * t)
y_62 = np.cos(2 * t) - 0.5 * np.cos(5 * t)
plot_knot(x_62, y_62, title="6₂ Knot Approximation", filename="images/knot_6_2.png")

# Approximation for knot 7_4
x_74 = np.sin(2 * t) - 0.7 * np.sin(5 * t)
y_74 = np.cos(3 * t) - 0.5 * np.cos(4 * t)
plot_knot(x_74, y_74, title="7₄ Knot Approximation", filename="images/knot_7_4.png")

plt.show()
