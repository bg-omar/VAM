# Diagram 7: Reconnectie en splijting (sequentiële illustratie van vortexsplitsing)
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import matplotlib.pyplot as plt
import numpy as np

# Setup plot grid
fig, axes = plt.subplots(1, 4, figsize=(16, 4), subplot_kw={'projection': '3d'})
titles = ["(a) Eén complexe knoop", "(b) Reconnectie-initiatief", "(c) Opsplitsing", "(d) Twee stabiele knopen"]

# Basisparametrie voor een torusvormige knoop
theta = np.linspace(0, 2 * np.pi, 500)
phi = np.linspace(0, 2 * np.pi, 500)
R = 2
r = 0.6

# Frames tonen knoop, opening, splitsing, los
for i, ax in enumerate(axes):
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_zlim(-3, 3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_title(titles[i])

    if i == 0:
        # Eén torusknoop
        x = (R + r * np.cos(3 * theta)) * np.cos(2 * theta)
        y = (R + r * np.cos(3 * theta)) * np.sin(2 * theta)
        z = r * np.sin(3 * theta)
        ax.plot(x, y, z, color='darkred', linewidth=2)

    elif i == 1:
        # Openingspunt – vortexvervorming
        x = (R + r * np.cos(3 * theta)) * np.cos(2 * theta)
        y = (R + r * np.cos(3 * theta)) * np.sin(2 * theta)
        z = r * np.sin(3 * theta)
        x[200:300] += 0.7  # lokale scheur
        ax.plot(x, y, z, color='orangered', linewidth=2)

    elif i == 2:
        # Twee gesplitste segmenten
        t1 = np.linspace(0, np.pi, 250)
        t2 = np.linspace(np.pi, 2 * np.pi, 250)
        for t, shift in zip([t1, t2], [-0.6, 0.6]):
            x = (R + r * np.cos(3 * t)) * np.cos(2 * t)
            y = (R + r * np.cos(3 * t)) * np.sin(2 * t)
            z = r * np.sin(3 * t) + shift
            ax.plot(x, y, z, linewidth=2, color='orange')

    elif i == 3:
        # Twee losse knopen
        t = np.linspace(0, 2 * np.pi, 500)
        x1 = (R + r * np.cos(3 * t)) * np.cos(2 * t) - 2
        y1 = (R + r * np.cos(3 * t)) * np.sin(2 * t)
        z1 = r * np.sin(3 * t)
        x2 = (R + r * np.cos(3 * t)) * np.cos(2 * t) + 2
        y2 = (R + r * np.cos(3 * t)) * np.sin(2 * t)
        z2 = r * np.sin(3 * t)
        ax.plot(x1, y1, z1, color='firebrick', linewidth=2)
        ax.plot(x2, y2, z2, color='firebrick', linewidth=2)


# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
# filename = f"{script_name}.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()

# Diagram 8: Multiknoop topologie — hoofdknoop met satellietknoop (neutronstructuur)

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Hoofdknoop (bijv. proton)
theta = np.linspace(0, 2 * np.pi, 500)
R = 2
r = 0.5
x_main = (R + r * np.cos(3 * theta)) * np.cos(2 * theta)
y_main = (R + r * np.cos(3 * theta)) * np.sin(2 * theta)
z_main = r * np.sin(3 * theta)
ax.plot(x_main, y_main, z_main, color='crimson', linewidth=2, label="Hoofdknoop (bijv. proton)")

# Satellietknoop (bijv. neutron) - kleine vortexring om hoofdstructuur
phi = np.linspace(0, 2 * np.pi, 200)
r_sat = 0.4
x_sat = r_sat * np.cos(phi) + 3.2
y_sat = r_sat * np.sin(phi)
z_sat = 0.2 * np.sin(2 * phi)
ax.plot(x_sat, y_sat, z_sat, color='navy', linewidth=2, label="Satellietknoop (bijv. neutron)")

# As- en stijlinstellingen
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])
ax.set_zlim([-2, 2])
ax.set_title("Multiknoopconfiguratie: Hoofdknoop + Satellietknoop")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.legend()
filename = f"8_multiknoop.pdf"
# plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"8_multiknoop.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()