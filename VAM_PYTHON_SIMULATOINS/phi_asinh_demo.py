import numpy as np

def golden_ratio_via_asinh():
    phi_exact = (1 + np.sqrt(5.0)) / 2.0
    phi_asinh = np.exp(np.arcsinh(0.5))  # asinh(1/2) -> ln(phi); exp(...) -> phi
    rel_err = abs(phi_asinh - phi_exact) / phi_exact
    print(f"phi_exact  = {phi_exact:.15f}")
    print(f"phi_asinh  = {phi_asinh:.15f}")
    print(f"relative error = {rel_err:.3e}")
    return phi_exact, phi_asinh, rel_err

if __name__ == '__main__':
    golden_ratio_via_asinh()