# -*- coding: utf-8 -*-
from __future__ import annotations
import os, json, argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from vam_infer.constants import load_constants
from vam_infer.inverse import fit_rc_from_tau, fit_rho_from_g
from vam_infer.models import tau_ratio, g_field
from vam_infer.io import load_tau_csv, load_g_csv

def main():
    ap = argparse.ArgumentParser(description="Fit VAM parameters from CSV data.")
    ap.add_argument("--tau", type=str, default=None, help="CSV with tau(r)")
    ap.add_argument("--g",   type=str, default=None, help="CSV with g(r)")
    ap.add_argument("--r-col", type=str, default=None, help="Name of radius column (if ambiguous)")
    ap.add_argument("--tau-col", type=str, default=None, help="Name of tau column (if ambiguous)")
    ap.add_argument("--g-col", type=str, default=None, help="Name of g column (if ambiguous)")
    ap.add_argument("--r-units", type=str, default="m", choices=["m","mm","um","nm"],
                    help="Units of r in CSV (scaled to meters).")
    ap.add_argument("--outdir", type=str, default="out_plots_csv", help="Output directory.")
    args = ap.parse_args()

    if args.tau is None and args.g is None:
        raise SystemExit("Provide at least one of --tau or --g.")

    unit_scale = {"m":1.0, "mm":1e-3, "um":1e-6, "nm":1e-9}[args.r_units]
    C = load_constants()

    os.makedirs(args.outdir, exist_ok=True)
    summary = {}

    # --- Fit r_c from tau(r) if provided ---
    if args.tau:
        r_tau, tau_obs = load_tau_csv(args.tau, r_col=args.r_col, tau_col=args.tau_col, r_scale=unit_scale)
        r_tau = np.asarray(r_tau, dtype=float)
        tau_obs = np.asarray(tau_obs, dtype=float)

        # Sort by r (log-log plotting looks nicer and model assumes monotone)
        idx = np.argsort(r_tau)
        r_tau, tau_obs = r_tau[idx], tau_obs[idx]

        rc_est = fit_rc_from_tau(r_tau, tau_obs, C)
        summary["r_c_est"] = rc_est

        # Plot
        plt.figure()
        plt.loglog(r_tau, tau_obs, ".", label="τ_obs")
        plt.loglog(r_tau, tau_ratio(r_tau, C), "-", label=f"τ_fit (r_c={C['r_c']['value']:.3e} m)")
        plt.xlabel("r [m]"); plt.ylabel("τ = dt_local/dt_∞"); plt.title("τ(r) fit")
        plt.grid(True, which="both"); plt.legend(); plt.tight_layout()
        plt.savefig(os.path.join(args.outdir, "tau_fit_csv.png")); plt.close()

    # --- Fit rho from g(r) if provided ---
    if args.g:
        r_g, g_obs = load_g_csv(args.g, r_col=args.r_col, g_col=args.g_col, r_scale=unit_scale)
        r_g = np.asarray(r_g, dtype=float)
        g_obs = np.asarray(g_obs, dtype=float)
        idx = np.argsort(r_g)
        r_g, g_obs = r_g[idx], g_obs[idx]

        rho_est = fit_rho_from_g(r_g, g_obs, C)
        summary["rho_ae_fluid_est"] = rho_est

        plt.figure()
        plt.loglog(r_g, g_obs, ".", label="g_obs")
        plt.loglog(r_g, g_field(r_g, C), "-", label=f"g_fit (ρ={C['rho_ae_fluid']['value']:.3e} kg/m³)")
        plt.xlabel("r [m]"); plt.ylabel("g(r) [m s$^{-2}$]"); plt.title("g(r) fit")
        plt.grid(True, which="both"); plt.legend(); plt.tight_layout()
        plt.savefig(os.path.join(args.outdir, "g_fit_csv.png")); plt.close()

    # --- Save summary
    with open(os.path.join(args.outdir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print("Summary:", summary)
    print(f"Wrote results to: {args.outdir}")

if __name__ == "__main__":
    main()
