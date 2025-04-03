import numpy as np
import matplotlib.pyplot as plt

# Grid setup
x = np.linspace(-3, 3, 300)
y = np.linspace(-2, 6, 400)
X, Y = np.meshgrid(x, y)

# New position of the wire (positive electrode)
wire_pos = np.array([0.0, 4.5])

# Foil: vertical line at x = 0 from y = -1.5 to 1.5
foil_x = 0.0
foil_y_min = -1.5
foil_y_max = 1.5

# Simulate field lines to follow a heart-like curvature
# We'll model the field as a potential from a point source, but with attraction to a vertical line (foil)

# Distance from wire
r_wire = np.sqrt((X - wire_pos[0])**2 + (Y - wire_pos[1])**2)
theta_wire = np.arctan2(Y - wire_pos[1], X - wire_pos[0])
E_wire_mag = 1 / (r_wire + 0.1)**2
E_wire_x = E_wire_mag * np.cos(theta_wire)
E_wire_y = E_wire_mag * np.sin(theta_wire)

# Add field curvature toward the centerline using a radial sink centered at the origin
r_sink = np.sqrt((X - foil_x)**2 + (Y)**2)
theta_sink = np.arctan2(Y, X - foil_x)
E_sink_mag = -1 / (r_sink + 0.1)
E_sink_x = E_sink_mag * np.cos(theta_sink)
E_sink_y = E_sink_mag * np.sin(theta_sink)

# Combine field components
E_total_x = E_wire_x + 1.5 * E_sink_x
E_total_y = E_wire_y + 1.5 * E_sink_y

# Plotting
plt.figure(figsize=(8, 10))
plt.streamplot(X, Y, E_total_x, E_total_y, color='blue', density=1.6, linewidth=1)
plt.plot(wire_pos[0], wire_pos[1], 'ro', label='Wire Electrode (+)')
plt.plot([foil_x, foil_x], [foil_y_min, foil_y_max], 'k--', linewidth=2, label='Foil Electrode (−)')
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Modified EHD Lifter Field Lines with Inward-Curving Flow")
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.xlim(-3, 3)
plt.ylim(-2, 6)
plt.tight_layout()



# Simulate attraction to full vertical foil by summing over line elements
E_foil_x = np.zeros_like(X)
E_foil_y = np.zeros_like(Y)

# Simulate vertical line of attraction with multiple segments
foil_segments = np.linspace(foil_y_min, foil_y_max, 50)
for y0 in foil_segments:
    r_seg = np.sqrt((X - foil_x)**2 + (Y - y0)**2)
    theta_seg = np.arctan2(Y - y0, X - foil_x)
    E_seg_mag = -1 / (r_seg + 0.1)**2
    E_foil_x += E_seg_mag * np.cos(theta_seg)
    E_foil_y += E_seg_mag * np.sin(theta_seg)

# Combine fields
E_total_x = E_wire_x + E_foil_x
E_total_y = E_wire_y + E_foil_y

# Plotting
plt.figure(figsize=(8, 10))
plt.streamplot(X, Y, E_total_x, E_total_y, color='blue', density=1.6, linewidth=1)
plt.plot(wire_pos[0], wire_pos[1], 'ro', label='Wire Electrode (+)')
plt.plot([foil_x, foil_x], [foil_y_min, foil_y_max], 'k--', linewidth=2, label='Foil Electrode (−)')
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("EHD Lifter Field Lines Aiming Toward Entire Foil")
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.xlim(-3, 3)
plt.ylim(-2, 6)
plt.tight_layout()
plt.show()