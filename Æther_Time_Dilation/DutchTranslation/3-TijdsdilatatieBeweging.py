import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
titles = ['(1) Deeltje in rust in æther', '(2) Deeltje in beweging met snelheid v']
omega_labels = [r'$\omega_0$', r'$\omega_{\mathrm{obs}} < \omega_0$']

for i, ax in enumerate(axes):
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(titles[i], fontsize=12)

    # Æther flow in moving case
    if i == 1:
        # Stroming rond vaste vortex geïnspireerd op stroomlijn rond cilinder
        x = np.linspace(-2, 2, 200)
        y = np.linspace(-1.8, 1.8, 200)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        THETA = np.arctan2(Y, X)

        # Potentiaal en stroomfunctie (uniforme stroming + dipool)
        U_inf = -1.0
        a = 1.0
        with np.errstate(divide='ignore', invalid='ignore'):
            psi = U_inf * (Y * (1 - (a**2) / (R**2)))
            u = U_inf * (1 - (a**2) * (X**2 - Y**2) / R**4)
            v = -2 * U_inf * a**2 * X * Y / R**4

        u[R < a] = np.nan
        v[R < a] = np.nan

        ax.streamplot(X, Y, u, v, color='navy', density=.4, arrowsize=1.5, linewidth=2.5, cmap='Blues', integration_direction='both')

        ax.text(0, 1.1, r'Ætherstroom $\vec{v}$ rond wervel', fontsize=12, ha='center', color='navy')
        # ax.text(1.3, 1.6, r'$|\vec{v}| = v$', fontsize=11, color='navy')

    # Draw vortex circle
    circle = plt.Circle((0, 0), 1, edgecolor='black', facecolor='lightblue', linewidth=2)
    ax.add_patch(circle)

    # Rotating marker
    theta = np.deg2rad(45)
    x_marker = np.cos(theta)
    y_marker = np.sin(theta)
    ax.plot(x_marker, y_marker, 'ro', markersize=20)

    # Tangentiële rotatiepijl op de rand van de vortex
    theta0 = np.pi / 4  # 45 graden
    r = 1.0
    x_start = r * np.cos(theta0)
    y_start = r * np.sin(theta0)

    # Richting loodrecht op radiusvector (d.w.z. tangentieel)
    dx = r * np.sin(theta0) * 0.5
    dy =  -r * np.cos(theta0) * 0.5



    # Rotation arrow (adjust length in moving case)
    if i == 0:
        ax.annotate('', xy=(x_start + dx, y_start + dy), xytext=(x_start, y_start),
                    arrowprops=dict(facecolor='red',  edgecolor='red', arrowstyle='->', linewidth=2))
    else:
        # Richting loodrecht op radiusvector (d.w.z. tangentieel)
        dx = r * np.sin(theta0) * 0.4
        dy =  -r * np.cos(theta0) * 0.4
        ax.annotate('', xy=(x_start + dx, y_start + dy), xytext=(x_start, y_start),
                    arrowprops=dict(facecolor='red',  edgecolor='red', arrowstyle='->', linewidth=2))

    ax.text(0.75 if i == 0 else 0.22, 0.3, omega_labels[i], fontsize=14)




# Caption
# plt.figtext(0.5, 0.01,
#             "Beweging door æther verlaagt de waargenomen hoeksnelheid $\omega_{\mathrm{obs}}$.",
#             wrap=True, horizontalalignment='center', fontsize=11)

plt.suptitle("Effect van ætherbeweging op rotatie van wervelkern", fontsize=14)
plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.show()