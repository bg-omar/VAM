import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from mpl_toolkits.mplot3d import Axes3D
import spherogram
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from mpl_toolkits.mplot3d import Axes3D

# --- Parse .fseries into a list of (header, coeff-dicts) blocks ---
def parse_fseries_multi(filename):
    knots = []
    header = None
    arrays = {k: [] for k in ('a_x','b_x','a_y','b_y','a_z','b_z')}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith('%'):
                # save previous if any
                if arrays['a_x']:
                    knots.append((header, {k: np.array(v) for k,v in arrays.items()}))
                    for v in arrays.values(): v.clear()
                header = line.lstrip('%').strip()
                continue
            if not line:
                continue
            parts = line.split()
            if len(parts)==6:
                for key,val in zip(arrays, map(float, parts)):
                    arrays[key].append(val)
    if arrays['a_x']:
        knots.append((header, {k: np.array(v) for k,v in arrays.items()}))
    return knots

# --- Evaluate Fourier block to a (N×3) array of xyz points ---
def eval_fourier_block(coeffs, s):
    x = y = z = np.zeros_like(s)
    for j in range(len(coeffs['a_x'])):
        n = j+1
        x += coeffs['a_x'][j]*np.cos(n*s) + coeffs['b_x'][j]*np.sin(n*s)
        y += coeffs['a_y'][j]*np.cos(n*s) + coeffs['b_y'][j]*np.sin(n*s)
        z += coeffs['a_z'][j]*np.cos(n*s) + coeffs['b_z'][j]*np.sin(n*s)
    return np.vstack([x,y,z]).T

# --- Load all knots, pick richest block ---
folder = 'fseries'
paths = sorted(glob.glob(os.path.join(folder,'*.fseries')))
labels = [os.path.basename(p) for p in paths]
s = np.linspace(0,2*np.pi,1000)

knots = []
for p in paths:
    blocks = parse_fseries_multi(p)
    if not blocks:
        knots.append(None)
    else:
        # pick block with max harmonics
        hdr, coeffs = max(blocks, key=lambda b: b[1]['a_x'].size)
        knots.append(eval_fourier_block(coeffs, s))

# --- Initial checkbox state (all on) ---
selected = [k is not None for k in knots]

# --- Set up the figure with checkboxes + empty 3D grid area ---
fig = plt.figure(figsize=(10,6))
rax = fig.add_axes([0.01,0.1,0.15,0.8])
check = CheckButtons(rax, labels, selected)

axes = []  # to store current 3D axes

def redraw(_):
    global axes
    # update selected flags
    for i,stat in enumerate(check.get_status()):
        selected[i] = stat

    # remove old axes
    for ax in axes:
        fig.delaxes(ax)
    axes.clear()

    # build list of active knots
    active = [k for k,sel in zip(knots,selected) if sel]
    if not active:
        fig.canvas.draw_idle()
        return

    # grid dims
    n = len(active)
    cols = int(np.ceil(np.sqrt(n)))
    rows = int(np.ceil(n/cols))

    # compute global limits so all loops fit
    allpts = np.vstack(active)
    L = np.max(np.abs(allpts))*1.1

    # create subplots
    for idx, pts in enumerate(active):
        ax = fig.add_subplot(rows,cols,idx+1,projection='3d')
        ax.plot(pts[:,0],pts[:,1],pts[:,2],color='slateblue',lw=1.5)
        ax.set_xlim(-L,L); ax.set_ylim(-L,L); ax.set_zlim(-L,L)
        ax.set_axis_off()
        axes.append(ax)

    plt.tight_layout(rect=[0.2,0,1,1])
    fig.canvas.draw_idle()

check.on_clicked(redraw)
redraw(None)
plt.show()
