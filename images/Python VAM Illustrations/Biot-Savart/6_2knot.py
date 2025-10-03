import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')


t = np.linspace(0, 2 * np.pi, 900)

# Standard parametric equations for 5_2 knot
x = (2 + np.cos(3 * t)) * np.cos(2 * t)
y = (2 + np.cos(3 * t)) * np.sin(2 * t)
z = np.sin(6 * t) + 0.3 * np.sin(3 * t)

fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot3D(x, y, z, color='deepskyblue', linewidth=2.5, label="6₂ Knot")
ax.set_title("6₂ Knot (Alexander–Briggs notation)", fontsize=15)
ax.set_axis_off()
ax.set_box_aspect([1, 1, 1])
ax.legend()
plt.show()