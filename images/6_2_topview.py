import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]


# Parametric equations for the (6,2) torus knot
def torus_knot(p=6, q=2, R=2.0, r=0.5, num_points=1000):
    t = np.linspace(0, 2 * np.pi, num_points)
    x = (R + r * np.cos(q * t)) * np.cos(p * t)
    y = (R + r * np.cos(q * t)) * np.sin(p * t)
    z = r * np.sin(q * t)
    return x, y, z

# Generate the knot
x, y, z = torus_knot()

# Plotting the top view (90° from above)
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
ax.plot(x, y, color='black', linewidth=1.5)
ax.set_aspect('equal')
ax.axis('off')
plt.title(r'$5_2$ Knot - Top View', fontsize=14)

# Save the figure
output_path = "knot_5_2_topview.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')



# Parametric equations for the (7,4) torus knot
def torus_knot_74(p=7, q=4, R=2.0, r=0.5, num_points=1500):
    t = np.linspace(0, 2 * np.pi, num_points)
    x = (R + r * np.cos(q * t)) * np.cos(p * t)
    y = (R + r * np.cos(q * t)) * np.sin(p * t)
    z = r * np.sin(q * t)
    return x, y, z

# Generate the knot
x, y, z = torus_knot_74()

# Plotting the top view (90° from above)
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
ax.plot(x, y, color='black', linewidth=1.5)
ax.set_aspect('equal')
ax.axis('off')
plt.title(r'$6_1$ Knot - Top View', fontsize=14)

# Save the figure
output_path = "knot_6_1_topview.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')


# Create 3D plots for the 5_2 and 6_1 knots
fig = plt.figure(figsize=(12, 6))

# 3D plot of 5_2 knot
ax1 = fig.add_subplot(121, projection='3d')
x6, y6, z6 = torus_knot(p=6, q=2)
ax1.plot3D(x6, y6, z6, color='black', linewidth=1.5)
ax1.set_title(r'$5_2$ Knot - 3D View', fontsize=14)
ax1.axis('off')

# 3D plot of 6_1 knot
ax2 = fig.add_subplot(122, projection='3d')
x7, y7, z7 = torus_knot_74(p=7, q=4)
ax2.plot3D(x7, y7, z7, color='black', linewidth=1.5)
ax2.set_title(r'$6_1$ Knot - 3D View', fontsize=14)
ax2.axis('off')

# Save the figure
output_path = "knots_5_2_and_6_1_3D.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')

fig = plt.figure(figsize=(6, 6))

# 5_2 Knot: Top view
ax1 = fig.add_subplot(421, projection='3d')
ax1.plot3D(x6, y6, z6, color='black', linewidth=1.2)
ax1.view_init(elev=89, azim=-90)
ax1.set_title(r'$5_2$ Knot - Top View', fontsize=12)
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("")            # no Z label
ax1.set_zticklabels([])       # no Z tick labels

# 5_2 Knot: Side view
ax2 = fig.add_subplot(422, projection='3d')
ax2.plot3D(x6, y6, z6, color='black', linewidth=1.2)
ax2.view_init(elev=40, azim=90)
ax2.set_title(r'$5_2$ Knot - Side View', fontsize=12)
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_zlabel("Z")

# 6_1 Knot: Top view
ax3 = fig.add_subplot(423, projection='3d')
ax3.plot3D(x7, y7, z7, color='black', linewidth=1.2)
ax3.view_init(elev=89, azim=-90)
ax3.set_title(r'$6_1$ Knot - Top View', fontsize=12)
ax3.set_xlabel("X")
ax3.set_ylabel("Y")
ax3.set_zlabel("")            # no Z label
ax3.set_zticklabels([])       # no Z tick labels

# 6_1 Knot: Side view
ax4 = fig.add_subplot(424, projection='3d')
ax4.plot3D(x7, y7, z7, color='black', linewidth=1.2)
ax4.view_init(elev=15, azim=25)
ax4.set_title(r'$6_1$ Knot - Side View', fontsize=12)
ax4.set_xlabel("")
ax4.set_ylabel("Y")
ax4.set_zlabel("Z")            # no Z label
ax4.set_xticklabels([])       # no Z tick labels

# Hide extra subplots (since only 4 used)
for i in range(4, 8):
    ax = fig.add_subplot(4, 2, i + 1)
    ax.axis('off')

plt.subplots_adjust(hspace=1.0, wspace=0.3)
# Save the figure
output_path = "knots_5_2_and_6_1_3D_views.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')


plt.show()
