import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend
# --- Knot parameterizations: all up to 7 crossings ---


def hopf_link_1(t):
    x = np.cos(t)
    y = np.sin(t)
    z = 0 * t
    return x, y, z

def hopf_link_2(t):
    x = 0 * t
    y = np.cos(t)
    z = np.sin(t)
    return x, y, z

def borromean_1(t):
    x = 2 * np.cos(t)
    y = 1.3 * np.sin(t)
    z = 0 * t
    return x, y, z

def borromean_2(t):
    x = 1.3 * np.sin(t)
    y = 0 * t
    z = 2 * np.cos(t)
    return x, y, z

def borromean_3(t):
    x = 0 * t
    y = 2 * np.cos(t)
    z = 1.3 * np.sin(t)
    return x, y, z




def solomon_link_components():
    """
    Returns a list of functions, each f(t), for the two components of the Solomon link.
    """
    def component1(t):
        x = (2 + np.cos(2*t)) * np.cos(4*t)
        y = (2 + np.cos(2*t)) * np.sin(4*t)
        z = np.sin(2*t)
        return x, y, z

    def component2(t):
        x = (2 + np.cos(2*t)) * np.cos(4*t)
        y = (2 + np.cos(2*t)) * np.sin(4*t)
        z = -np.sin(2*t)
        return x, y, z

    return [component1, component2]



def torus_knot(p, q, R=2.0, r=0.5, num_points=1000):
    """
    Generate a torus knot with parameters (p, q).
    p: number of twists around the major circle
    q: number of twists around the minor circle
    R: major radius (distance from center of tube to center of torus)
    r: minor radius (radius of tube)
    num_points: number of points in the knot
    """
    t = np.linspace(0, 2 * np.pi, num_points)
    x = (R + r * np.cos(q * t)) * np.cos(p * t)
    y = (R + r * np.cos(q * t)) * np.sin(p * t)
    z = r * np.sin(q * t)
    return x, y, z

def canonical_3_knot(n):
    """
    Returns a function f(t) for the 3-crossing knot n (only 1: the trefoil knot).
    - 3_1: Trefoil knot (canonical (2,3) torus knot)
    """
    if n == 1:
        # Trefoil (3₁)
        return lambda t: (
            (2 + np.cos(3*t)) * np.cos(2*t),
            (2 + np.cos(3*t)) * np.sin(2*t),
            np.sin(3*t)
        )
    else:
        # Trefoil (3₁)
        return lambda t: (
            (2 + np.cos(2*t)) * np.cos(3*t),
            (2 + np.cos(2*t)) * np.sin(3*t),
            np.sin(2*t)
        )




def canonical_4_knot(n):
    """
    Returns a function f(t) for the 4-crossing knot n (only 1: the figure-eight knot).
    - 4_1: Figure-eight knot (standard Lissajous/Fourier)
    """
    if n == 1:
        return lambda t: (
            (2 + np.cos(2*t)) * np.cos(3*t),
            (2 + np.cos(2*t)) * np.sin(3*t),
            np.sin(4*t)
        )
    else:
        raise ValueError("n must be 1 for the 4-crossing knots (figure-eight).")


def canonical_5_knot(n):
    """
    Returns a function f(t) for the 5-crossing knot n (1 or 2).
    - 5_1: (5,2) torus knot
    - 5_2: Lissajous/Fourier style
    """
    if n == 1:
        # 5_1 (5,2) torus knot
        return lambda t: (
            (2 + np.cos(2*t)) * np.cos(5*t),
            (2 + np.cos(2*t)) * np.sin(5*t),
            np.sin(2*t)
        )
    elif n == 2:
        # 5_2 (Lissajous/Fourier)
        return lambda t: (
            np.cos(2*t) + 0.3 * np.cos(3*t),
            np.sin(3*t),
            np.sin(5*t)
        )
    else:
        raise ValueError("n must be 1 or 2 for the 5-crossing knots.")


def canonical_6_knot(n):
    """
    Returns a function f(t) for the 6-crossing knot n (1..3).
    - 6_1: Stevedore's knot
    - 6_2: Lissajous/Fourier style
    - 6_3: (6,5) torus knot
    """
    if n == 1:
        # 6_1 Stevedore's knot (Lissajous/Fourier)
        return lambda t: (
            np.cos(3*t) + 0.5 * np.cos(6*t),
            np.sin(4*t),
            np.sin(6*t)
        )
    elif n == 2:
        # 6_2 (Lissajous/Fourier)
        return lambda t: (
            np.cos(2*t) + 0.5 * np.cos(4*t),
            np.sin(3*t),
            np.sin(5*t)
        )
    elif n == 3:
        # 6_3 (6,5) torus knot
        return lambda t: (
            (2 + np.cos(5*t)) * np.cos(6*t),
            (2 + np.cos(5*t)) * np.sin(6*t),
            np.sin(5*t)
        )
    else:
        raise ValueError("n must be in 1..3 for the 6-crossing knots.")


def canonical_7_knot(n):
    """
    Returns a function f(t) giving x, y, z for the canonical 6- or 7-crossing knot number n.
    n: integer (1 through 7)
    """
    if n == 1:
        # 7_1 (7,2) torus knot
        return lambda t: (
            (2 + np.cos(2*t)) * np.cos(7*t),
            (2 + np.cos(2*t)) * np.sin(7*t),
            np.sin(2*t)
        )
    elif n == 2:
        # 7_2 (Lissajous/Fourier style)
        return lambda t: (
            np.cos(2*t) + 0.4 * np.cos(5*t),
            np.sin(3*t),
            np.sin(7*t)
        )
    elif n == 3:
        # 7_3 (7,3) torus knot
        return lambda t: (
            (2 + np.cos(3*t)) * np.cos(7*t),
            (2 + np.cos(3*t)) * np.sin(7*t),
            np.sin(3*t)
        )
    elif n == 4:
        # 7_4 (7,4) torus knot
        return lambda t: (
            (2 + np.cos(4*t)) * np.cos(7*t),
            (2 + np.cos(4*t)) * np.sin(7*t),
            np.sin(4*t)
        )
    elif n == 5:
        # 7_5 (7,5) torus knot
        return lambda t: (
            (2 + np.cos(5*t)) * np.cos(7*t),
            (2 + np.cos(5*t)) * np.sin(7*t),
            np.sin(5*t)
        )
    elif n == 6:
        # 7_6 (7,6) torus knot
        return lambda t: (
            (2 + np.cos(6*t)) * np.cos(7*t),
            (2 + np.cos(6*t)) * np.sin(7*t),
            np.sin(6*t)
        )
    elif n == 7:
        # 7_7 (Lissajous/Fourier style)
        return lambda t: (
            np.cos(3*t) + 0.6 * np.cos(5*t),
            np.sin(4*t),
            np.sin(7*t)
        )
    else:
        raise ValueError("n must be in 1..7 for the 7-crossing knots.")

# Usage example:
t = np.linspace(0, 2*np.pi, 800)
knotnum = 4  # for 7_4
x, y, z = canonical_7_knot(knotnum)(t)



# --- Knot list (name, function, color) ---
knot_funcs = [
    ("$3_1$ (trefoil)", canonical_3_knot(1), 'red'),
    ("$4_1$ (figure-eight)", canonical_4_knot(1), 'orange'),
    ("$5_1$", canonical_5_knot(1), 'gold'),
    ("$5_2$", canonical_5_knot(2), 'green'),
    ("$6_1$", canonical_6_knot(1), 'deepskyblue'),
    ("$6_2$", canonical_6_knot(2), 'blue'),
    ("$6_3$", canonical_6_knot(3), 'purple'),
    ("$7_1$", canonical_7_knot(1), 'magenta'),
    ("$7_2$", canonical_7_knot(2), 'brown'),
    ("$7_3$", canonical_7_knot(3), 'chocolate'),
    ("$7_4$", canonical_7_knot(4), 'teal'),
    ("$7_5$", canonical_7_knot(5), 'olive'),
    ("$7_6$", canonical_7_knot(6), 'crimson'),
    ("$7_7$", canonical_7_knot(7), 'black'),
]

t = np.linspace(0, 2 * np.pi, 950)
n_knots = len(knot_funcs)
ncols = 4
nrows = (n_knots + ncols - 1) // ncols

fig = plt.figure(figsize=(ncols * 3.3, nrows * 3.1))
for i, (label, func, color) in enumerate(knot_funcs):
    ax = fig.add_subplot(nrows, ncols, i + 1, projection='3d')
    x, y, z = func(t)
    ax.plot3D(x, y, z, color=color, linewidth=2.2, label=label)
    ax.set_title(label, fontsize=13, pad=6)
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 1])
    ax.legend(loc="upper left", fontsize=10, handlelength=1)
    ax.view_init(elev=37, azim=45 + i * 10)  # slight unique view


import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2*np.pi, 800)
components = solomon_link_components()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for func, color in zip(components, ['red', 'blue']):
    x, y, z = func(t)
    ax.plot(x, y, z, lw=2, color=color)

ax.set_axis_off()

import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2*np.pi, 800)
borromean = [borromean_1, borromean_2, borromean_3]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for func, color in zip(borromean, ['red', 'green', 'blue']):
    x, y, z = func(t)
    ax.plot(x, y, z, lw=2, color=color)

ax.set_axis_off()

plt.tight_layout()
plt.show()



import numpy as np

def get_knot_or_link(kind, n=None):
    """
    Returns a list of functions [f1, f2, ...] for the components of the chosen knot or link.
    For knots, the list has one function.
    For links, the list has one function per component.
    """
    # TREFOIL
    if kind.lower() == 'trefoil':
        return [lambda t: (
            (2 + np.cos(3*t)) * np.cos(2*t),
            (2 + np.cos(3*t)) * np.sin(2*t),
            np.sin(3*t)
        )]
    # FIGURE EIGHT (4_1)
    elif kind.lower() in ['figure8', 'figure-eight', '4_1', 'knot4']:
        return [lambda t: (
            (2 + np.cos(2*t)) * np.cos(3*t),
            (2 + np.cos(2*t)) * np.sin(3*t),
            np.sin(4*t)
        )]
    # 5-CROSSING KNOTS
    elif kind.lower() in ['5', 'knot5']:
        if n == 1:
            # 5_1 torus knot
            return [lambda t: (
                (2 + np.cos(2*t)) * np.cos(5*t),
                (2 + np.cos(2*t)) * np.sin(5*t),
                np.sin(2*t)
            )]
        elif n == 2:
            # 5_2 Lissajous
            return [lambda t: (
                np.cos(2*t) + 0.3 * np.cos(3*t),
                np.sin(3*t),
                np.sin(5*t)
            )]
        else:
            raise ValueError("For kind='knot5', n must be 1 or 2.")
    # 6-CROSSING KNOTS
    elif kind.lower() in ['6', 'knot6']:
        if n == 1:
            return [lambda t: (
                np.cos(3*t) + 0.5 * np.cos(6*t),
                np.sin(4*t),
                np.sin(6*t)
            )]
        elif n == 2:
            return [lambda t: (
                np.cos(2*t) + 0.5 * np.cos(4*t),
                np.sin(3*t),
                np.sin(5*t)
            )]
        elif n == 3:
            return [lambda t: (
                (2 + np.cos(5*t)) * np.cos(6*t),
                (2 + np.cos(5*t)) * np.sin(6*t),
                np.sin(5*t)
            )]
        else:
            raise ValueError("For kind='knot6', n must be 1, 2, or 3.")
    # 7-CROSSING KNOTS
    elif kind.lower() in ['7', 'knot7']:
        if n == 1:
            return [lambda t: (
                (2 + np.cos(2*t)) * np.cos(7*t),
                (2 + np.cos(2*t)) * np.sin(7*t),
                np.sin(2*t)
            )]
        elif n == 2:
            return [lambda t: (
                np.cos(2*t) + 0.4 * np.cos(5*t),
                np.sin(3*t),
                np.sin(7*t)
            )]
        elif n == 3:
            return [lambda t: (
                (2 + np.cos(3*t)) * np.cos(7*t),
                (2 + np.cos(3*t)) * np.sin(7*t),
                np.sin(3*t)
            )]
        elif n == 4:
            return [lambda t: (
                (2 + np.cos(4*t)) * np.cos(7*t),
                (2 + np.cos(4*t)) * np.sin(7*t),
                np.sin(4*t)
            )]
        elif n == 5:
            return [lambda t: (
                (2 + np.cos(5*t)) * np.cos(7*t),
                (2 + np.cos(5*t)) * np.sin(7*t),
                np.sin(5*t)
            )]
        elif n == 6:
            return [lambda t: (
                (2 + np.cos(6*t)) * np.cos(7*t),
                (2 + np.cos(6*t)) * np.sin(7*t),
                np.sin(6*t)
            )]
        elif n == 7:
            return [lambda t: (
                np.cos(3*t) + 0.6 * np.cos(5*t),
                np.sin(4*t),
                np.sin(7*t)
            )]
        else:
            raise ValueError("For kind='knot7', n must be 1..7.")
    # SOLOMON LINK (2,4 torus link)
    elif kind.lower() in ['solomon', '2_4', 'solomonlink']:
        def solomon1(t):
            x = (2 + np.cos(2*t)) * np.cos(4*t)
            y = (2 + np.cos(2*t)) * np.sin(4*t)
            z = np.sin(2*t)
            return x, y, z
        def solomon2(t):
            return solomon1(t + np.pi)
        return [solomon1, solomon2]
    # HOPF LINK
    elif kind.lower() in ['hopf', 'hopflink']:
        def hopf1(t):
            x = np.cos(t)
            y = np.sin(t)
            z = 0 * t
            return x, y, z
        def hopf2(t):
            x = 0 * t
            y = np.cos(t)
            z = np.sin(t)
            return x, y, z
        return [hopf1, hopf2]
    # BORROMEAN RINGS (three ellipses in perpendicular planes)
    elif kind.lower() in ['borromean', 'borromeanrings', 'borromean rings']:
        def bor1(t):
            x = 2 * np.cos(t)
            y = 1.3 * np.sin(t)
            z = 0 * t
            return x, y, z
        def bor2(t):
            x = 1.3 * np.sin(t)
            y = 0 * t
            z = 2 * np.cos(t)
            return x, y, z
        def bor3(t):
            x = 0 * t
            y = 2 * np.cos(t)
            z = 1.3 * np.sin(t)
            return x, y, z
        return [bor1, bor2, bor3]
    else:
        raise ValueError("Unknown knot/link type.")






import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2*np.pi, 800)

# EXAMPLES:
# Trefoil
fns = get_knot_or_link('trefoil')
# Figure-eight
# fns = get_knot_or_link('figure8')
# 5_2
# fns = get_knot_or_link('knot5', n=2)
# Solomon
# fns = get_knot_or_link('solomon')
# Hopf
# fns = get_knot_or_link('hopf')
# Borromean
# fns = get_knot_or_link('borromean')

colors = ['red', 'blue', 'green', 'purple', 'orange', 'black', 'magenta']
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for fn, color in zip(fns, colors):
    x, y, z = fn(t)
    ax.plot(x, y, z, lw=2, color=color)
ax.set_axis_off()
plt.show()


def chain_link_1(t):
    x = 2*np.cos(t)
    y = np.sin(t)
    z = 0*t
    return x, y, z
def chain_link_2(t):
    x = 2*np.cos(t)
    y = -np.sin(t)
    z = 0*t + 1.5  # Offset in z
    return x, y, z
def chain_link_3(t):
    x = 0*t
    y = 2*np.cos(t)
    z = np.sin(t) + 0.75  # Offset in z
    return x, y, z


def borromean_link():
    def bor1(t):
        x = 2 * np.cos(t)
        y = 1.3 * np.sin(t)
        z = 0 * t
        return x, y, z
    def bor2(t):
        x = 1.3 * np.sin(t)
        y = 0 * t
        z = 2 * np.cos(t)
        return x, y, z
    def bor3(t):
        x = 0 * t
        y = 2 * np.cos(t)
        z = 1.3 * np.sin(t)
        return x, y, z
    return [bor1, bor2, bor3]

def three_component_chain():
    def ch1(t):
        x = 2 * np.cos(t)
        y = np.sin(t)
        z = 0 * t
        return x, y, z
    def ch2(t):
        x = 2 * np.cos(t)
        y = -np.sin(t)
        z = 0 * t + 1.5
        return x, y, z
    def ch3(t):
        x = 0 * t
        y = 2 * np.cos(t)
        z = np.sin(t) + 0.75
        return x, y, z
    return [ch1, ch2, ch3]


import numpy as np
import matplotlib.pyplot as plt

def hopf_link_component(t, shift):
    # Major radius R, minor radius r (for torus)
    R = 2.0
    r = 0.7
    # Parametric angle for circle
    theta = t
    # Each ring shifted by 0, 2pi/3, 4pi/3
    phi = shift
    x = (R + r * np.cos(theta)) * np.cos(phi) - r * np.sin(theta) * np.sin(phi)
    y = (R + r * np.cos(theta)) * np.sin(phi) + r * np.sin(theta) * np.cos(phi)
    z = r * np.sin(theta)
    return x, y, z

# Create 3 rings, each shifted by 120°
shifts = [0, 2*np.pi/3, 4*np.pi/3]
t = np.linspace(0, 2*np.pi, 500)
colors = ['red', 'green', 'blue']

fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, projection='3d')
for phi, color in zip(shifts, colors):
    x, y, z = hopf_link_component(t, phi)
    ax.plot(x, y, z, lw=3, color=color)

ax.set_box_aspect([1,1,1])
ax.set_axis_off()
plt.tight_layout()
plt.show()
