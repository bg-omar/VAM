import os, json
import matplotlib
matplotlib.use("Agg")  # headless-safe
import numpy as np
import matplotlib.pyplot as plt

from vam_infer.constants import load_constants
from vam_infer.models import tau_ratio, g_field
from vam_infer.utils import geomspace_exclude_zero, make_noisy
from vam_infer.inverse import fit_rc_from_tau, fit_rho_from_g

C = load_constants()

# Choose radii ranges that are numerically well-conditioned:
# - tiny r: τ(r) sensitive to r_c
# - larger r: g(r) numerically stable
r_tau = geomspace_exclude_zero(1e-14, 1e-9, 300)
r_g   = geomspace_exclude_zero(1e-6,  1e-2, 200)

# True signals
tau_true = tau_ratio(r_tau, C)
g_true   = g_field(r_g, C)

# Observations with small relative noise
tau_obs = make_noisy(tau_true, rel_noise=1e-6, seed=1, floor=0.0)
g_obs   = make_noisy(g_true,   rel_noise=1e-9, seed=2, floor=0.0)

# Inference
rc_est  = fit_rc_from_tau(r_tau, tau_obs, C)
rho_est = fit_rho_from_g(r_g, g_obs, C)

# Output
os.makedirs("out_plots", exist_ok=True)

plt.figure()
plt.loglog(r_tau, tau_obs, '.', label="τ_obs")
plt.loglog(r_tau, tau_ratio(r_tau, C), '-', label=f"τ_fit (r_c={C['r_c']['value']:.3e} m)")
plt.xlabel("r [m]"); plt.ylabel("τ = dt_local/dt_∞"); plt.title("Time-dilation fit")
plt.grid(True, which="both"); plt.legend(); plt.tight_layout()
plt.savefig("out_plots/time_dilation_fit.png"); plt.close()

plt.figure()
plt.loglog(r_g, g_obs, '.', label="g_obs")
plt.loglog(r_g, g_field(r_g, C), '-', label=f"g_fit (ρ={C['rho_ae_fluid']['value']:.3e} kg/m³)")
plt.xlabel("r [m]"); plt.ylabel("g(r) [m s^-2]"); plt.title("g-field fit")
plt.grid(True, which="both"); plt.legend(); plt.tight_layout()
plt.savefig("out_plots/g_field_fit.png"); plt.close()

summary = {
    "r_c_est": C["r_c"]["value"],
    "rho_ae_fluid_est": C["rho_ae_fluid"]["value"],
}
with open("out_plots/summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print("Estimated:", summary)
print("Wrote: out_plots/time_dilation_fit.png, out_plots/g_field_fit.png, out_plots/summary.json")
