from sympy import symbols, Matrix, I, simplify, Eq, pprint

# Define symbolic swirl operators as 2x2 matrices (analogous to Pauli matrices)
# These represent chirality flip, twist, and reconnection as simplified operators
S1 = Matrix([[0, 1], [1, 0]])             # Chirality flip (like sigma_x)
S2 = Matrix([[0, -I], [I, 0]])            # Twist (like sigma_y)
S3 = Matrix([[1, 0], [0, -1]])            # Reconnection mutation (like sigma_z)

# Compute commutators
comm_S1_S2 = S1 * S2 - S2 * S1
comm_S2_S3 = S2 * S3 - S3 * S2
comm_S3_S1 = S3 * S1 - S1 * S3

# Expected SU(2) structure: [Si, Sj] = 2i * Sk for Pauli matrices
expected_comm_S1_S2 = 2 * I * S3
expected_comm_S2_S3 = 2 * I * S1
expected_comm_S3_S1 = 2 * I * S2

# Check if the commutators match expected SU(2) structure
eq1 = Eq(comm_S1_S2, expected_comm_S1_S2)
eq2 = Eq(comm_S2_S3, expected_comm_S2_S3)
eq3 = Eq(comm_S3_S1, expected_comm_S3_S1)

print(comm_S1_S2)
print( comm_S2_S3)
print( comm_S3_S1)
print( eq1)
print( eq2)
print( eq3)


a, b, c = symbols('a b c')
S1_gen = Matrix([
    [0, a, 0],
    [a, 0, 0],
    [0, 0, 0]
])

S2_gen = Matrix([
    [0, -I*b, 0],
    [I*b, 0, 0],
    [0, 0, 0]
])

S3_gen = Matrix([
    [c, 0, 0],
    [0, -c, 0],
    [0, 0, 0]
])

# Compute commutators for generalized swirl operators
comm_S1_S2_gen = simplify(S1_gen * S2_gen - S2_gen * S1_gen)
comm_S2_S3_gen = simplify(S2_gen * S3_gen - S3_gen * S2_gen)
comm_S3_S1_gen = simplify(S3_gen * S1_gen - S1_gen * S3_gen)

print(comm_S1_S2_gen)
print(comm_S2_S3_gen)
print(comm_S3_S1_gen)
