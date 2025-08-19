import numpy as np

def omega_swirl(r, C):
    r"""Ω(r)=(C_e/r_c)\,e^{-r/r_c}"""
    Ce, rc = C["C_e"]["value"], C["r_c"]["value"]
    return (Ce/rc) * np.exp(-r/rc)

def tau_ratio(r, C):
    r"""τ(r)=sqrt(1-Ω(r)^2/c^2) with clipping for numerical safety."""
    c = C["c"]["value"]
    arg = 1.0 - (omega_swirl(r, C)**2)/(c**2)
    arg = np.clip(arg, 0.0, 1.0)
    return np.sqrt(arg)

def M_eff(r, C):
    r"""M_eff(r)=∫_0^r 4π r'^2 ρ_ae e^{-r'/r_c}dr' = 4πρ[2r_c^3 - e^{-r/r_c}(r^2 r_c + 2 r r_c^2 + 2 r_c^3)]"""
    rho, rc = C["rho_ae_fluid"]["value"], C["r_c"]["value"]
    term = 2*rc**3 - np.exp(-r/rc) * ((r**2)*rc + 2*r*rc**2 + 2*rc**3)
    return 4.0*np.pi*rho*term

def g_field(r, C):
    r"""g(r)=G_swirl M_eff(r)/r^2"""
    Gs = C["G_swirl"]["value"]
    with np.errstate(divide="ignore", invalid="ignore"):
        g = Gs * M_eff(r, C) / (r**2)
        g = np.where(r==0, 0.0, g)
    return g


