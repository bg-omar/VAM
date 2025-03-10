

# Re-import necessary libraries since execution state was reset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define view angles and parameters
view_angles = [(20, -20)] * 3 + [(30, -20)] * 3  # Three for normal, three for swirled versions
titles = [
    "Ring Torus Diagram (R=1.5 > r=1)", "Horn Torus Diagram (R = 1 = r)", "Swindle Torus Diagram (R=1/2 < r=1)",
    "Swirl Ring Torus", "Swirl Horn Torus", "Swirl Swindle Torus"
]
radii = [(1.5, 1), (1, 1), (0.5, 1), (1.5, 1), (1, 1), (0.5, 1)]

# Define helical parameters
num_helix_turns = 3
torus_revolutions = 5  # The number of full toroidal cycles before restarting
helix_theta = np.linspace(0, torus_revolutions * 2 * np.pi, 72 * num_helix_turns)
winding_ratio = 2 + 2 / 5  # Ensures 12 windings per full torus cycle
helix_phi = winding_ratio * helix_theta

# Create figure with 2x3 subplots
fig, axes = plt.subplots(1, 2, figsize=(15, 10), subplot_kw={'projection': '3d'})

for ax, (elev, azim), title, (R, r) in zip(axes.flatten(), view_angles, titles, radii):
    # Generate torus mesh
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, 2 * np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)

    X = (R + r * np.cos(phi)) * np.cos(theta)
    Y = (R + r * np.cos(phi)) * np.sin(theta)
    Z = r * np.sin(phi)

    # Swirl transformation for second row
    swirl_factor = 1/12 * np.pi / max(Z.flatten())
    X_swirl = X * np.cos(swirl_factor * Z) - Y * np.sin(swirl_factor * Z)
    Y_swirl = X * np.sin(swirl_factor * Z) + Y * np.cos(swirl_factor * Z)

    # Compute three helical coils (corrected phase shifts)
    helices = []
    for i in range(3):
        phase_shift = i * (2 * np.pi / 3)  # Phase shift applied evenly
        helix_x = (R + r * np.cos(helix_phi + phase_shift)) * np.cos(helix_theta + phase_shift)
        helix_y = (R + r * np.cos(helix_phi + phase_shift)) * np.sin(helix_theta + phase_shift)
        helix_z = r * np.sin(helix_phi + phase_shift)
        helices.append((helix_x, helix_y, helix_z))

    # Plot torus with or without swirl
    if "Swirl" in title:
        ax.plot_surface(X_swirl, Y_swirl, Z, rstride=5, cstride=5, color='lightblue', alpha=0.08, edgecolor='k')
    else:
        ax.plot_surface(X, Y, Z, rstride=5, cstride=5, color='lightblue', alpha=0.08, edgecolor='k')

    # Plot three-phase helical windings
    colors = ['r', 'b', 'g']
    width = [1, 0, 0]
    for i, (helix_x, helix_y, helix_z) in enumerate(helices):
        ax.plot(helix_x, helix_y, helix_z, color=colors[i], linewidth=width[i], label=f"Phase {i+1}")

    # Set view, limits, and labels
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title(title)
    ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio

plt.tight_layout()
plt.show()

#
# # Re-import necessary libraries since execution state was reset
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
#
# # Define view angles and parameters
# view_angles = [(20, -20)] * 3 + [(30, -20)] * 3  # Three for normal, three for swirled versions
# titles = [
#     "Ring Torus Diagram (R=1.5 > r=1)", "Horn Torus Diagram (R = 1 = r)", "Swindle Torus Diagram (R=1/2 < r=1)",
#     "Swirl Ring Torus", "Swirl Horn Torus", "Swirl Swindle Torus"
# ]
# radii = [(1.5, 1), (1, 1), (0.5, 1), (1.5, 1), (1, 1), (0.5, 1)]
#
# # Define helical parameters
# num_helix_turns = 3
# torus_revolutions = 4  # The number of full toroidal cycles before restarting
# helix_theta = np.linspace(0, torus_revolutions * 2 * np.pi, 72 * num_helix_turns)
# winding_ratio = 2 + 2 / 5  # Ensures 12 windings per full torus cycle
# helix_phi = winding_ratio * helix_theta
#
# # Create figure with 2x3 subplots
# fig, axes = plt.subplots(2, 3, figsize=(15, 10), subplot_kw={'projection': '3d'})
#
# for ax, (elev, azim), title, (R, r) in zip(axes.flatten(), view_angles, titles, radii):
#     # Generate torus mesh
#     theta = np.linspace(0, 2 * np.pi, 100)
#     phi = np.linspace(0, 2 * np.pi, 100)
#     theta, phi = np.meshgrid(theta, phi)
#
#     X = (R + r * np.cos(phi)) * np.cos(theta)
#     Y = (R + r * np.cos(phi)) * np.sin(theta)
#     Z = r * np.sin(phi)
#
#     # Swirl transformation for second row
#     swirl_factor = 1/12 * np.pi / max(Z.flatten())
#     X_swirl = X * np.cos(swirl_factor * Z) - Y * np.sin(swirl_factor * Z)
#     Y_swirl = X * np.sin(swirl_factor * Z) + Y * np.cos(swirl_factor * Z)
#
#     # Compute three helical coils
#     helices = []
#     for i in range(3):
#         phase_shift = i * (2 * np.pi / 3)
#         helix_x = (R + r * np.cos(helix_phi)) * np.cos(helix_theta + phase_shift)
#         helix_y = (R + r * np.cos(helix_phi)) * np.sin(helix_theta + phase_shift)
#         helix_z = r * np.sin(helix_phi + phase_shift)
#         helices.append((helix_x, helix_y, helix_z))
#
#     # Plot torus with or without swirl
#     if "Swirl" in title:
#         ax.plot_surface(X_swirl, Y_swirl, Z, rstride=5, cstride=5, color='lightblue', alpha=0.08, edgecolor='k')
#     else:
#         ax.plot_surface(X, Y, Z, rstride=5, cstride=5, color='lightblue', alpha=0.08, edgecolor='k')
#
#     # Plot three-phase helical windings
#     colors = ['r', 'b', 'g']
#     for i, (helix_x, helix_y, helix_z) in enumerate(helices):
#         ax.plot(helix_x, helix_y, helix_z, color=colors[i], linewidth=2, label=f"Phase {i+1}")
#
#     # Set view, limits, and labels
#     ax.view_init(elev=elev, azim=azim)
#     ax.set_xlim(-2, 2)
#     ax.set_ylim(-2, 2)
#     ax.set_zlim(-2, 2)
#     ax.set_xlabel('X-axis')
#     ax.set_ylabel('Y-axis')
#     ax.set_zlabel('Z-axis')
#     ax.set_title(title)
#     ax.set_box_aspect([1, 1, 1])  # Ensures 1:1:1 aspect ratio
#
# plt.tight_layout()
# plt.show()
