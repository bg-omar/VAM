import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# Use TkAgg backend
matplotlib.use('TkAgg')

import os

script_name = os.path.splitext(os.path.basename(__file__))[0]

# Adjustable resolution / total points for different knots
TOTAL_POINTS = 500  # Change this for higher precision or larger knots
SEG_PARTS = 2
# Parameter range for the trefoil knot; adjust the 4π for different scaling
t = np.linspace(0, 4 * np.pi, TOTAL_POINTS)

# Knot parameters
p, q = 7, 1  # Trefoil knot parameters
r = 1  # minor radius
R = r * 2.618
# Parametric equations for the trefoil knot
x = (R + r * np.cos(p * t)) * np.cos(q * t)
y = (R + r * np.cos(p * t)) * np.sin(q * t)
z = r * np.sin(p * t)

# Prepare 3D figure
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_xlim([-4, 4])
ax.set_ylim([-4, 4])
ax.set_zlim([-2, 2])
ax.axis('off')  # Remove axes, grid and labels
ax.view_init(elev=90, azim=0)  # Top-down view

# For easy access later, pre-calculate the full set of points (each row is one 3D coordinate)
points_all = np.vstack((x, y, z)).T

# Define the visible segment length (here, a quarter of total points)
segment_length = TOTAL_POINTS // SEG_PARTS

# Initialize the Line3DCollection with an empty set of segments.
# We'll update its segments and scalar array (for the colormap) in each frame.
lc = Line3DCollection([], cmap='Blues', linewidth=2)
ax.Line3DCollection(lc)


# Animation update function
def update(frame):
    # Let frame run from 0 to TOTAL_POINTS-1; add offset for smooth looping with a fixed visible segment
    # The visible segment indices wrap around using modulo arithmetic.
    indices = (frame + np.arange(segment_length)) % TOTAL_POINTS

    # Get the visible points from the full knot
    visible_points = points_all[indices]

    # Create segments from the visible points (each segment connects point i to i+1)
    # new_segments will be of shape (N-1, 2, 3)
    new_segments = np.concatenate([visible_points[:-1, None, :],
                                   visible_points[1:, None, :]], axis=1)

    # Set these segments to the 3D collection.
    lc.set_segments(new_segments)

    # Create a fade effect by generating a scalar array to pass to the colormap.
    # Values here go from 0.2 (faded) to 1.0 (fully opaque) along the segment.
    fade = np.linspace(0.2, 1.0, len(new_segments))
    lc.set_array(fade)

    return (lc,)


# Create animation: here we run frames from 0 to TOTAL_POINTS, looping the parameter
ani = animation.FuncAnimation(fig, update, frames=TOTAL_POINTS, interval=20, blit=False)
writer_mp4 = animation.FFMpegWriter(fps=60, extra_args=['-vcodec', 'libx264'])
ani.save(f"{script_name}.mp4", writer=writer_mp4)


writer_gif = animation.PillowWriter(fps=60)
ani.save(f"{script_name}.gif", writer=writer_gif)

plt.show()