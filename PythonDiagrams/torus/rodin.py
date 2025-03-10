import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

num_turns=10
num_points=1000
theta = np.linspace(0, num_turns * 2 * np.pi, num_points)
phi = (2 + 2/5) * theta  # Adjusted winding ratio for Rodin pattern
# Function to generate Rodin coil windings
def generate_rodin_coil(R, r, num_turns=12, num_points=1000):
    """
    Generate Rodin coil windings in a toroidal coordinate system.

    Parameters:
    R -- Major radius of the torus
    r -- Minor radius of the torus
    num_turns -- Number of full turns around the torus
    num_points -- Resolution of the coil path

    Returns:
    x, y, z -- Coordinates of the Rodin coil winding
    """
    theta = np.linspace(0, num_turns * 2 * np.pi, num_points)
    phi = (2 + 2/5) * theta  # Adjusted winding ratio for Rodin pattern

    # Compute Rodin coil path
    x = (R + r * np.cos(phi)) * np.cos(theta)
    y = (R + r * np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)
    return x, y, z

# Function to generate 3-phase shifted windings
def generate_rodin_3phase(R, r, num_turns=10, num_points=1000):
    """
    Generate 3-phase interwoven Rodin coil windings.

    Returns:
    Three sets of x, y, z coordinates corresponding to phase shifts of 120° each.
    """
    x1, y1, z1 = generate_rodin_coil(R, r, num_turns, num_points)
    x2, y2, z2 = generate_rodin_coil(R, r, num_turns, num_points)
    x3, y3, z3 = generate_rodin_coil(R, r, num_turns, num_points)

    # Apply 120-degree phase shifts
    theta_shift = 2 * np.pi / 3
    x2 = (R + r * np.cos(phi + theta_shift)) * np.cos(theta + theta_shift)
    y2 = (R + r * np.cos(phi + theta_shift)) * np.sin(theta + theta_shift)
    z2 = r * np.sin(phi + theta_shift)

    x3 = (R + r * np.cos(phi - theta_shift)) * np.cos(theta - theta_shift)
    y3 = (R + r * np.cos(phi - theta_shift)) * np.sin(theta - theta_shift)
    z3 = r * np.sin(phi - theta_shift)

    return (x1, y1, z1), (x2, y2, z2), (x3, y3, z3)

# Function to plot the Rodin coil and its variations
def plot_rodin_coil():
    R, r = 1.5, 1  # Set torus major and minor radii

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Plot 3-phase Rodin coil windings
    (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = generate_rodin_3phase(R, r)
    ax.plot(x1, y1, z1, 'r-', linewidth=2, label="Phase 1")
    ax.plot(x2, y2, z2, 'b-', linewidth=2, label="Phase 2")
    ax.plot(x3, y3, z3, 'g-', linewidth=2, label="Phase 3")

    # Plot toroidal frame
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, 2 * np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)

    X = (R + r * np.cos(phi)) * np.cos(theta)
    Y = (R + r * np.cos(phi)) * np.sin(theta)
    Z = r * np.sin(phi)

    ax.plot_wireframe(X, Y, Z, color='gray', alpha=0.2, linewidth=0.5)


    # Set plot labels
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title("Optimized 3-Phase Rodin Coil")

    # Set equal aspect ratio
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_box_aspect([1,1,1])
    ax.legend()
    plt.show()

# Generate and plot the optimized Rodin coil
plot_rodin_coil()
