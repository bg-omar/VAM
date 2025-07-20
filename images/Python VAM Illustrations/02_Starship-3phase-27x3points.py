import numpy as np

import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# Corrected and clear visualization with sequences explicitly plotted and labeled with different colors and tints

rotation_steps=0
rotation_angle = (2 * np.pi / 27) / 3
# Define provided base sequence
base_sequence = [1, 5, 9, 4, 8, 3, 7, 2, 6, 1]

# Create explicit sequences as per user request
sequence_A_forward = [((num * 3 - 0 - 1) % 27) + 1 for num in base_sequence]
sequence_A_neutral = [((num * 3 - 0 - 1) % 27) + 1 for num in base_sequence]
sequence_A_backward = [((num * 3 - 0 - 1) % 27) + 1 for num in base_sequence]

sequence_B_forward = [((num * 3 - 1 - 1) % 27) + 1 for num in base_sequence]
sequence_B_neutral = [((num * 3 - 1 - 1) % 27) + 1 for num in base_sequence]
sequence_B_backward = [((num * 3 - 1 - 1) % 27) + 1 for num in base_sequence]

sequence_C_forward = [((num * 3 - 2 - 1) % 27) + 1 for num in base_sequence]
sequence_C_neutral = [((num * 3 - 2 - 1) % 27) + 1 for num in base_sequence]
sequence_C_backward = [((num * 3 - 2 - 1) % 27) + 1 for num in base_sequence]

# Points setup
angles = np.linspace(0, 2 * np.pi, 28)[:-1]
positions = {i+1: (np.cos(angle), np.sin(angle)) for i, angle in enumerate(angles)}
segment_shift = ((2 * np.pi / 27) / 3)


# Recalculate positions with adjusted angles for rotation and reversed numbering
angles_rotated = np.linspace(0, 2 * np.pi, 28)[:-1] - np.pi*1.5 +(2*np.pi*(1/27)) # Rotate 90° counterclockwise
angles_rotated = angles_rotated[::-1]  # Reverse numbering for clockwise count
positions_rotated = {i+1: (np.cos(angle), np.sin(angle)) for i, angle in enumerate(angles_rotated)}


angles_rotated += rotation_angle

# Plot setup
plt.figure(figsize=(14, 14))
plt.axis('equal')

def plot_rotated_wire(sequence, segment, base_color, style, label, alpha=1.0):
    for i in range(len(sequence)-1):
        num = sequence[i]
        next_num = sequence[i+1]

        # Apply rotation offset here:
        angle_start = angles_rotated[(num - 1 + rotation_steps) % 27] + segment_shift * (segment - 1)
        angle_end = angles_rotated[(next_num - 1 + rotation_steps) % 27] + segment_shift * (segment - 1)

        x_start, y_start = np.cos(angle_start), np.sin(angle_start)
        x_end, y_end = np.cos(angle_end), np.sin(angle_end)

        plt.plot([x_start, x_end], [y_start, y_end],
                 color=base_color, linestyle=style, linewidth=2, alpha=alpha, label=label if i == 0 else "")


# Phase A (Blue)
plot_rotated_wire(sequence_A_forward, 1, 'blue', '-', 'Phase A Forward', alpha=0.9)
plot_rotated_wire(sequence_A_neutral, 2, 'blue', '--', 'Phase A Neutral', alpha=0.1)
plot_rotated_wire(sequence_A_backward, 3, 'blue', '-', 'Phase A Backward', alpha=0.7)

# Phase B (Red)
plot_rotated_wire(sequence_B_forward, 1, 'red', '-', 'Phase B Forward', alpha=0.9)
plot_rotated_wire(sequence_B_neutral, 2, 'red', '--', 'Phase B Neutral', alpha=0.1)
plot_rotated_wire(sequence_B_backward, 3, 'red', '-', 'Phase B Backward', alpha=0.7)

# Phase C (Green)
plot_rotated_wire(sequence_C_forward, 1, 'green', '-', 'Phase C Forward', alpha=0.9)
plot_rotated_wire(sequence_C_neutral, 2, 'green', '--', 'Phase C Neutral', alpha=0.1)
plot_rotated_wire(sequence_C_backward, 3, 'green', '-', 'Phase C Backward', alpha=0.7)

# Draw clearly numbered main points with rotated positions
for num, (x, y) in positions_rotated.items():
    plt.plot(x, y, 'ko', markersize=6)
    plt.text(x * 1.05, y * 1.05, str(num), fontsize=10, ha='center', va='center')

# Adjustments and display
plt.legend()
plt.title("3-Phase Rodin Coil", fontsize=16)
plt.grid(True)


# ✅ Get the script filename dynamically
import os
from datetime import datetime
script_name = os.path.splitext(os.path.basename(__file__))[0]
timestamp = datetime.now().strftime("%H%M%S")
filename = f"{script_name}_{timestamp}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()
