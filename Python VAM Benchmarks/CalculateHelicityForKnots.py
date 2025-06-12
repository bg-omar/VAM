import math

# Constants
r_c = 1.40897017e-15         # m
C_e = 1.09384563e6           # m/s
pi = math.pi

# Circulation Gamma = 2π * r_c * C_e
Gamma = 2 * pi * r_c * C_e

# Torus link T(18,27)
N = 9  # Number of components
SL_k = 3  # Self-linking for each trefoil
Lk_ij = 1  # Pairwise linking number

# Total helicity H = sum self + sum mutual
self_helicity = N * (Gamma**2) * SL_k
mutual_helicity = sum([2 * Gamma**2 * Lk_ij for _ in range(N * (N - 1) // 2)])
total_helicity = self_helicity + mutual_helicity

print(self_helicity)
print(mutual_helicity)
print(total_helicity)
