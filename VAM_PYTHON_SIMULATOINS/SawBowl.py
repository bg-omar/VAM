# Re-run after reset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.widgets import RadioButtons

S = 40
p = 4
plate_diameter = 0.12
R_end = plate_diameter/2.0
R_start = 0.03
height = 0.015
turns = 2
power = 2.618
star_offset_mech_deg = 15.0

thetas = np.linspace(0, 2*np.pi, S, endpoint=False)

step_fwd, step_back = 11, 9
def step_walk(S, n_steps):
    idx = 0
    seq = [idx]
    for k in range(n_steps):
        if k % 2 == 0:
            idx = (idx + step_fwd) % S
        else:
            idx = (idx - step_back) % S
        seq.append(idx)
    return np.array(seq, dtype=int)

pairs_per_turn = S//2
n_pairs = turns * pairs_per_turn
seq = step_walk(S, n_pairs*2)

t = np.linspace(0, 1, len(seq))
r = R_end - (R_end - R_start) * (t**power)
z = height * (1.0 - t)

def path_xyz(seq, thetas, r_of_t, z_of_t, samples_per_seg=24, theta_offset_deg=0.0):
    theta_offset = np.deg2rad(theta_offset_deg)
    xs, ys, zs = [], [], []
    for k in range(len(seq)-1):
        i0, i1 = seq[k], seq[k+1]
        th0 = thetas[i0] + theta_offset
        th1 = thetas[i1] + theta_offset
        dth = (th1 - th0 + np.pi) % (2*np.pi) - np.pi
        th_line = th0 + np.linspace(0, 1, samples_per_seg, endpoint=False) * dth
        r_line = np.linspace(r_of_t[k], r_of_t[k+1], samples_per_seg, endpoint=False)
        z_line = np.linspace(z_of_t[k], z_of_t[k+1], samples_per_seg, endpoint=False)
        xs.append(r_line * np.cos(th_line))
        ys.append(r_line * np.sin(th_line))
        zs.append(z_line)
    return np.concatenate(xs), np.concatenate(ys), np.concatenate(zs)

xA, yA, zA = path_xyz(seq, thetas, r, z, samples_per_seg=24, theta_offset_deg=0.0)
xB, yB, zB = path_xyz(seq, thetas, r, z, samples_per_seg=24, theta_offset_deg=star_offset_mech_deg)

fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(R_end*np.cos(thetas), R_end*np.sin(thetas), np.zeros_like(thetas), s=8)
ax.plot(xA, yA, zA, linewidth=1.8, label='SawShapeCoil — Star A')
ax.plot(xB, yB, zB, linewidth=1.2, label='SawShapeCoil — Star B (+15° mech)')

ax.set_title("SawShapeCoil (S=40, +11/−9) — Bowl-shaped layering (3D)")
ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.set_zlabel("z (m)")
ax.set_box_aspect([1,1,0.6])
ax.view_init(elev=24, azim=45)
ax.legend(loc='upper left')

lims = np.array([ax.get_xlim3d(), ax.get_ylim3d()]).reshape(2,2)
xy_max = np.max(np.abs(lims))
ax.set_xlim3d([-xy_max, xy_max]); ax.set_ylim3d([-xy_max, xy_max])

outpath = "SawShapeCoil_S40_bowl_3D.png"
plt.tight_layout(); plt.savefig(outpath, dpi=220, bbox_inches='tight')
plt.show()

