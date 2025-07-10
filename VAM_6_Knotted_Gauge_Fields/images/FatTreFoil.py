# Re-run after reset: Trefoil knot with tangential quiver placement
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

import math
import os
import re
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.pyplot as plt
import numpy as np

# ✅ Get the script filename dynamically
import os
from datetime import datetime


# Trefoil knot parametric centerline
theta = np.linspace(0, 2 * np.pi, 300)
x = (2 + np.cos(3 * theta)) * np.cos(2 * theta)
y = (2 + np.cos(3 * theta)) * np.sin(2 * theta)
z = np.sin(3 * theta)

# Parameters for tube surface (vortex core)
tube_radius = 0.3
n_circle = 12  # resolution of the circular cross-section
phi = np.linspace(0, 2 * np.pi, n_circle)
circle_x = tube_radius * np.cos(phi)
circle_y = tube_radius * np.sin(phi)

# Create 3D tube coordinates
tube_x, tube_y, tube_z = [], [], []
quiver_pos = 150  # mid point for quiver placement
quiver_point = None
quiver_tangent = None

for i in range(len(x)):
    # approximate local tangent
    if i < len(x) - 1:
        dx, dy, dz = x[i+1] - x[i], y[i+1] - y[i], z[i+1] - z[i]
    else:
        dx, dy, dz = x[i] - x[i-1], y[i] - y[i-1], z[i] - z[i-1]
    tangent = np.array([dx, dy, dz])
    tangent /= np.linalg.norm(tangent)
    # generate two orthogonal vectors
    normal = np.cross(tangent, [0, 0, 1])
    if np.linalg.norm(normal) == 0:
        normal = np.cross(tangent, [0, 1, 0])
    normal /= np.linalg.norm(normal)
    binormal = np.cross(tangent, normal)
    binormal /= np.linalg.norm(binormal)
    # build the ring
    ring_x = x[i] + circle_x * normal[0] + circle_y * binormal[0]
    ring_y = y[i] + circle_x * normal[1] + circle_y * binormal[1]
    ring_z = z[i] + circle_x * normal[2] + circle_y * binormal[2]
    tube_x.append(ring_x)
    tube_y.append(ring_y)
    tube_z.append(ring_z)

    if i == quiver_pos:
        quiver_point = (x[i], y[i], z[i])
        quiver_tangent = tangent
#
# # Plot the tube
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')
#
# # Quiver: Tangential velocity Ce at mid-point
# if quiver_point and quiver_tangent is not None:
#     ax.quiver(quiver_point[0], quiver_point[1], quiver_point[2],
#               quiver_tangent[0], quiver_tangent[1], quiver_tangent[2],
#               color='crimson', length=5.0, normalize=True, linewidth=5,
#               label='Tangential Velocity $C_e$')
#
# # Create surface segments
# for i in range(len(tube_x) - 1):
#     for j in range(n_circle - 1):
#         verts = [
#             [tube_x[i][j], tube_y[i][j], tube_z[i][j]],
#             [tube_x[i+1][j], tube_y[i+1][j], tube_z[i+1][j]],
#             [tube_x[i+1][j+1], tube_y[i+1][j+1], tube_z[i+1][j+1]],
#             [tube_x[i][j+1], tube_y[i][j+1], tube_z[i][j+1]]
#         ]
#         poly = Poly3DCollection([verts], color=plt.cm.plasma(i / len(tube_x)), linewidths=0.05, edgecolor='gray')
#         ax.add_collection3d(poly)
#
# # Final plot adjustments
# ax.set_xlim([-4, 4])
# ax.set_ylim([-4, 4])
# ax.set_zlim([-2.5, 2.5])
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# ax.set_title('Trefoil Knot with Physical Vortex Core (radius $r_c$)')
#
# ax.legend()
# plt.tight_layout()
# plt.show()



import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QSlider, QLabel,
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def torus(R, r, u, v):
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    return x, y, z

def rotate_xyz(x, y, z, rx, ry, rz):
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(rx), -np.sin(rx)],
                   [0, np.sin(rx), np.cos(rx)]])
    Ry = np.array([[np.cos(ry), 0, np.sin(ry)],
                   [0, 1, 0],
                   [-np.sin(ry), 0, np.cos(ry)]])
    Rz = np.array([[np.cos(rz), -np.sin(rz), 0],
                   [np.sin(rz), np.cos(rz), 0],
                   [0, 0, 1]])
    R = Rz @ Ry @ Rx
    xyz = np.vstack((x.flatten(), y.flatten(), z.flatten()))
    rotated = R @ xyz
    return rotated[0].reshape(x.shape), rotated[1].reshape(y.shape), rotated[2].reshape(z.shape)

class RingControl(QWidget):
    def __init__(self, name, update_callback):
        super().__init__()
        self.update_callback = update_callback
        self.name = name
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        # Parameters: x, y, z, rx, ry, rz
        self.sliders = {}
        self.labels = {}

        params = [
            ('x', 0, -100, 100),
            ('y', 0, -100, 100),
            ('z', 0, -100, 100),
            ('rx', 0, 0, 360),
            ('ry', 0, 0, 360),
            ('rz', 0, 0, 360),
        ]

        for i, (param, default, minv, maxv) in enumerate(params):
            label = QLabel(f"{self.name} {param}: {default / 10 if param in ['x','y','z'] else default}")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(minv)
            slider.setMaximum(maxv)
            slider.setValue(default)
            slider.valueChanged.connect(self.slider_changed)
            self.sliders[param] = slider
            self.labels[param] = label
            layout.addWidget(label, i, 0)
            layout.addWidget(slider, i, 1)

        self.setLayout(layout)

    def slider_changed(self):
        for param, slider in self.sliders.items():
            val = slider.value()
            if param in ['x', 'y', 'z']:
                disp_val = val / 10
            else:
                disp_val = val
            self.labels[param].setText(f"{self.name} {param}: {disp_val}")
        self.update_callback()

    def get_params(self):
        p = {}
        for param, slider in self.sliders.items():
            val = slider.value()
            if param in ['x', 'y', 'z']:
                p[param] = val / 10.0
            else:
                p[param] = np.radians(val)
        return p

class RingPlotter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('3D Linked Rings Controller with Global Size')

        layout = QHBoxLayout()
        self.setLayout(layout)

        # Left: Controls
        controls_layout = QVBoxLayout()

        # Global size controls
        size_group = QGroupBox("Global Size Controls")
        size_layout = QGridLayout()

        self.slider_R = QSlider(Qt.Horizontal)
        self.slider_R.setMinimum(5)    # 0.5 * 10
        self.slider_R.setMaximum(50)   # 5.0 * 10
        self.slider_R.setValue(30)     # default 3.0 * 10
        self.slider_R.valueChanged.connect(self.update_plot)
        self.label_R = QLabel("R: 3.0")

        self.slider_r = QSlider(Qt.Horizontal)
        self.slider_r.setMinimum(1)    # 0.1 * 10
        self.slider_r.setMaximum(20)   # 2.0 * 10
        self.slider_r.setValue(10)     # default 1.0 * 10
        self.slider_r.valueChanged.connect(self.update_plot)
        self.label_r = QLabel("r: 1.0")

        size_layout.addWidget(self.label_R, 0, 0)
        size_layout.addWidget(self.slider_R, 0, 1)
        size_layout.addWidget(self.label_r, 1, 0)
        size_layout.addWidget(self.slider_r, 1, 1)
        size_group.setLayout(size_layout)

        controls_layout.addWidget(size_group)

        # Rings controls
        self.ring1 = RingControl("Ring 1", self.update_plot)
        self.ring2 = RingControl("Ring 2", self.update_plot)
        self.ring3 = RingControl("Ring 3", self.update_plot)

        controls_layout.addWidget(self.ring1)
        controls_layout.addWidget(self.ring2)
        controls_layout.addWidget(self.ring3)

        layout.addLayout(controls_layout, 1)

        # Right: Matplotlib Figure
        self.fig = Figure(figsize=(8, 8))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas, 3)

        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_box_aspect([1,1,1])
        self.ax.axis('off')

        self.u = np.linspace(0, 2*np.pi, 100)
        self.v = np.linspace(0, 2*np.pi, 50)
        self.u, self.v = np.meshgrid(self.u, self.v)

        self.update_plot()

    def update_plot(self):
        # Update labels for size sliders
        self.label_R.setText(f"R: {self.slider_R.value() / 10:.2f}")
        self.label_r.setText(f"r: {self.slider_r.value() / 10:.2f}")

        R_global = self.slider_R.value() / 10.0
        r_global = self.slider_r.value() / 10.0

        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_box_aspect([1,1,1])
        self.ax.set_xlim([-10, 10])
        self.ax.set_ylim([-10, 10])
        self.ax.set_zlim([-10, 10])

        for ring_control, color in zip(
                [self.ring1, self.ring2, self.ring3],
                ['red', 'green', 'blue']
        ):
            p = ring_control.get_params()
            x, y, z = torus(R_global, r_global, self.u, self.v)
            x, y, z = rotate_xyz(x, y, z, p['rx'], p['ry'], p['rz'])
            self.ax.plot_surface(x + p['x'], y + p['y'], z + p['z'], color=color, alpha=0.7)

        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    ex = RingPlotter()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()