import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')


# Torus parameters
R = 1.0  # Major radius (distance from center of tube to center of torus)
r = 0.3  # Minor radius (radius of tube)

p, q = 7, 4  # (p,q) torus knot

theta = np.linspace(0, 2 * np.pi, 800)

# Parametric equations for (p, q) torus knot
x = (R + r * np.cos(q * theta)) * np.cos(p * theta)
y = (R + r * np.cos(q * theta)) * np.sin(p * theta)
z = r * np.sin(q * theta)

fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot3D(x, y, z, color='magenta', linewidth=2.5, label="K(7,4) Knot")
ax.set_title("K(7,4) Torus Knot", fontsize=16)
ax.set_axis_off()
ax.set_box_aspect([1, 1, 1])
ax.legend()
plt.show()
