import numpy as np

# VAM constants (from user-set values)
C_e = 1093845.63          # m/s
r_c = 1.40897017e-15        # m

phi = (1 + np.sqrt(5.0)) / 2.0

# Golden rapidity and derived quantities
xi_g = 1.5 * np.log(phi)      # ξ_g = (3/2) ln φ
beta_g = np.tanh(xi_g)        # should equal 1/φ

v_g = beta_g * C_e            # golden tangential velocity
Omega = C_e / r_c
Omega_g = v_g / r_c           # golden swirl frequency

def main():
    print("phi               =", repr(phi))
    print("xi_g              =", repr(xi_g))
    print("beta_g=tanh(xi_g) =", repr(beta_g))
    print("1/phi             =", repr(1.0/phi))
    print("C_e [m/s]         =", repr(C_e))
    print("r_c [m]           =", repr(r_c))
    print("v_g [m/s]         =", repr(v_g))
    print("C_e/phi [m/s]     =", repr(C_e/phi))
    print("Omega [1/s]       =", repr(Omega))
    print("Omega_g [1/s]     =", repr(Omega_g))
    # identity checks
    print("rel.err beta      =", abs(beta_g - 1.0/phi)/(1.0/phi))
    print("rel.err v_g       =", abs(v_g - C_e/phi)/(C_e/phi))
    print("rel.err Omega_g   =", abs(Omega_g - Omega/phi)/(Omega/phi))

if __name__ == "__main__":
    main()