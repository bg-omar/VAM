import numpy as np
from .models import tau_ratio, g_field

def fit_rc_from_tau(r, tau_obs, C):
    """Grid + local refine on r_c."""
    rc0 = C["r_c"]["value"]
    grid = np.geomspace(rc0*0.1, rc0*10.0, 200)
    best_rc, best_err = rc0, 1e99
    for trial in grid:
        C["r_c"]["value"] = trial
        err = float(np.mean((tau_obs - tau_ratio(r, C))**2))
        if err < best_err:
            best_err, best_rc = err, trial
    for _ in range(6):
        lo, hi = best_rc*0.8, best_rc*1.2
        for trial in np.geomspace(lo, hi, 41):
            C["r_c"]["value"] = trial
            err = float(np.mean((tau_obs - tau_ratio(r, C))**2))
            if err < best_err:
                best_err, best_rc = err, trial
    C["r_c"]["value"] = best_rc
    return best_rc, best_err

def fit_rho_from_g(r, g_obs, C):
    """
    Linear scale fit with normalization to avoid underflow:
      rho* = (A·g)/(A·A), where A = g(r; rho=1).
    """
    # Build A with rho=1
    C1 = {k: {"value": v["value"], "unit": v.get("unit","")} for k,v in C.items()}
    C1["rho_ae_fluid"]["value"] = 1.0
    A = g_field(r, C1)

    scale = float(np.max(np.abs(A))) or 1.0
    A_s = A/scale; g_s = g_obs/scale
    num = float(np.dot(A_s, g_s))
    den = float(np.dot(A_s, A_s)) or 1.0
    rho_est = num/den

    C["rho_ae_fluid"]["value"] = rho_est
    # report mse
    pred = g_field(r, C)/scale
    mse = float(np.mean((pred - g_s)**2))
    return rho_est, mse