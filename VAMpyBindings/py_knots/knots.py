import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D plotting
import spherogram
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]



def parse_fseries_multi(filename):
    """Parse a .fseries file, yielding (header, coeffs) for each block."""
    knots = []
    current_header = None
    a_x, b_x, a_y, b_y, a_z, b_z = [], [], [], [], [], []
    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('%'):
                if a_x:  # save previous block
                    knots.append((current_header, (
                        np.array(a_x), np.array(b_x),
                        np.array(a_y), np.array(b_y),
                        np.array(a_z), np.array(b_z)
                    )))
                    a_x, b_x, a_y, b_y, a_z, b_z = [], [], [], [], [], []
                current_header = line.lstrip('%').strip() or None
                continue
            if not line:
                if a_x:  # end of block, save
                    knots.append((current_header, (
                        np.array(a_x), np.array(b_x),
                        np.array(a_y), np.array(b_y),
                        np.array(a_z), np.array(b_z)
                    )))
                    a_x, b_x, a_y, b_y, a_z, b_z = [], [], [], [], [], []
                current_header = None
                continue
            parts = line.split()
            if len(parts) == 3:  # skip xyz lines
                continue
            if len(parts) == 6:
                ax, bx, ay, by, az, bz = map(float, parts)
                a_x.append(ax)
                b_x.append(bx)
                a_y.append(ay)
                b_y.append(by)
                a_z.append(az)
                b_z.append(bz)
    if a_x:  # last block
        knots.append((current_header, (
            np.array(a_x), np.array(b_x),
            np.array(a_y), np.array(b_y),
            np.array(a_z), np.array(b_z)
        )))
    return knots

def eval_fourier(a_x, b_x, a_y, b_y, a_z, b_z, s):
    x = np.zeros_like(s)
    y = np.zeros_like(s)
    z = np.zeros_like(s)
    N = len(a_x)
    for j in range(N):
        n = j + 1
        x += a_x[j]*np.cos(n*s) + b_x[j]*np.sin(n*s)
        y += a_y[j]*np.cos(n*s) + b_y[j]*np.sin(n*s)
        z += a_z[j]*np.cos(n*s) + b_z[j]*np.sin(n*s)
    return x, y, z

def plot_knots_grid(filenames):
    # Parse all knots and count the max number of versions
    all_knots = [parse_fseries_multi(fname) for fname in filenames]
    max_versions = max(len(knots) for knots in all_knots)
    n_files = len(filenames)

    fig, axs = plt.subplots(n_files, max_versions,
                            figsize=(5*max_versions, 4*n_files),
                            subplot_kw={'projection': '3d'},
                            squeeze=False)
    s = np.linspace(0, 2*np.pi, 1000)

    for row, (fname, knot_blocks) in enumerate(zip(filenames, all_knots)):
        knot_name = os.path.splitext(os.path.basename(fname))[0]
        for col in range(max_versions):
            ax = axs[row, col]
            if col < len(knot_blocks):
                header, (a_x, b_x, a_y, b_y, a_z, b_z) = knot_blocks[col]
                x, y, z = eval_fourier(a_x, b_x, a_y, b_y, a_z, b_z, s)
                ax.plot(x, y, z, lw=2, color='slateblue')
                title = header if header else f"Version {col+1}"
                ax.set_title(title, fontsize=11)
            else:
                ax.axis('off')
            # Visual tweaks
            ax.set_axis_off()
            ax.set_box_aspect([1,1,1])
        # Leftmost: label the row with the knot filename
        axs[row, 0].annotate(
            knot_name, xy=(0, 0.5), xytext=(-0.23, 0.5),
            textcoords='axes fraction', ha='center', va='center',
            fontsize=14, fontweight='bold', rotation=90, color='gray'
        )
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # USAGE: python plot_knots.py file1.fseries file2.fseries ...
    # For Jupyter or copy-paste, just edit the list below:
    filenames = [
        "fseries/knot.3_1.fseries",
        "fseries/knot.4_1.fseries",
        "fseries/knot.6_2.fseries",
        "fseries/knot.7_4.fseries",
    ]
    # Uncomment below to use sys.argv:
    # if len(sys.argv) < 2:
    #     print("Usage: python plot_knots.py file1.fseries file2.fseries ...")
    #     sys.exit(1)
    # filenames = sys.argv[1:]
    plot_knots_grid(filenames)
