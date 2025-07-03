import math, numpy as np, pandas as pd
import ace_tools_open as tools
from constants import a_0

# ─── Lord Kelvin ────────────────────────────────────────────────────────────────
# Mathematical expressions translated to Python functions
# 𝐾 = knot number (e.g. torus winding count or twist number),
# 𝑁 = number of vortex threads (vortex cores),
# 𝑎 = ring major radius (loop center offset),
# 𝑟 = ring tube radius (core radius),
# 𝜇 = rotational angular momentum,
# 𝐼 = impulse (linear or swirl momentum density × volume),
# 𝑍 rings = ring layers or stackings per unit length.
def tan_kelvin(I, N, mu, K, pi=math.pi):
    # tan(phi) = sqrt( I**1.5 / (N * mu * K**0.5 * pi**0.5) )
    return math.sqrt(I**(3/2) / (N * mu * K**0.5 * pi**0.5))

def tan_phi_kelvin(a, N, r):
    # tan(phi) = (2 * pi * a / N) * (1 / (2 * pi * r))
    return (2 * math.pi * a / N) * (1 / (2 * math.pi * r))

def I_impuls_ring(Z_rings, K, a):
    # I_impuls = Z_rings * K * pi * a**2
    return Z_rings * K * math.pi * a**2

def mu_rot_momentum(K, N, r, a):
    # mu_RotMomentum = K * N * pi * r**2 * a
    return K * N * math.pi * r**2 * a

def a_squared(I, K, pi=math.pi):
    # a^2 = I / (K * pi)
    return I / (K * pi)

def r_squared(mu, N, K, I, pi=math.pi):
    # r^2 = mu / (N * K * (1/2) * pi**(1/2) * I**(1/2))
    return mu / (N * K * 0.5 * pi**0.5 * I**0.5)

def tan_phi_formula_3(I, N, mu, K, Z_rings, pi=math.pi):
    # tan(phi) = sqrt( (1/Z_rings) * I**1.5 / (N * mu * K**0.5 * pi**0.5) )
    return math.sqrt((1/Z_rings) * I**(3/2) / (N * mu * K**0.5 * pi**0.5))
# ─── Lord Kelvin ────────────────────────────────────────────────────────────────
