#!/usr/bin/env python3
import numpy as np, pandas as pd, argparse, json
from math import log
# Physical constants
h = 6.62607015e-34
kB = 1.380649e-23
c = 299_792_458.0

def planck_lambda(lambda_m, T):
    lam = np.asarray(lambda_m)
    x = (h*c)/(lam*kB*T)
    ex = np.exp(np.clip(x, 1e-9, 1e2))
    return (1.0/(lam**5)) * (1.0/(ex - 1.0))

def freefree_lambda(lambda_m, T):
    lam = np.asarray(lambda_m)
    x = (h*c)/(lam*kB*T)
    ex = np.exp(-np.clip(x, 0, 1e2))
    return (1.0/(lam**2)) * ex

def fit_spectrum_lambda(lam_nm, I, model="planck", T_grid=(4000, 60000, 500)):
    lam_m = lam_nm * 1e-9
    I = I.astype(float)
    T_min, T_max, T_step = T_grid
    Ts = np.arange(T_min, T_max + 1e-9, T_step, dtype=float)
    best = None
    n = len(I)
    for T in Ts:
        f = planck_lambda(lam_m, T) if model=="planck" else freefree_lambda(lam_m, T)
        f = f/np.max(f)
        X = np.vstack([f, np.ones_like(f)]).T
        A, B = np.linalg.lstsq(X, I, rcond=None)[0]
        fit = A*f + B
        resid = I - fit
        RSS = float(resid @ resid)
        k_params = 3
        AIC = 2*k_params + n*np.log(RSS/n + 1e-300)
        if (best is None) or (RSS < best["RSS"]):
            best = dict(T_best=float(T), A=float(A), B=float(B), RSS=float(RSS), AIC=float(AIC))
    return best

def frac_shift(alpha, p_int, chi, u_ae):
    return 3.0 * np.log(alpha) * chi * (u_ae / p_int)

def main():
    ap = argparse.ArgumentParser(description="SBSL–VAM minimal fitter and improbability test")
    ap.add_argument("--alpha", type=float, required=True, help="R0/Rmin (dimensionless) assumed equal for both runs")
    ap.add_argument("--pA", type=float, required=True, help="Interior pressure of run A in Pa")
    ap.add_argument("--pB", type=float, required=True, help="Interior pressure of run B in Pa")
    ap.add_argument("--chi", type=float, default=1.0, help="VAM coupling factor (0..1 typically)")
    ap.add_argument("--u_ae", type=float, required=True, help="VAM swirl energy density in Pa (0.5*rho_ae*C_e^2)")
    ap.add_argument("--csvA", type=str, required=True, help="CSV for run A with columns lambda_nm,I")
    ap.add_argument("--csvB", type=str, required=True, help="CSV for run B with columns lambda_nm,I")
    ap.add_argument("--model", choices=["planck","freefree"], default="planck")
    ap.add_argument("--Tmin", type=float, default=4000)
    ap.add_argument("--Tmax", type=float, default=60000)
    ap.add_argument("--dT", type=float, default=500)
    ap.add_argument("--out", type=str, default="vam_fit_results.json")
    args = ap.parse_args()

    dfA = pd.read_csv(args.csvA)
    dfB = pd.read_csv(args.csvB)
    lamA, IA = dfA["lambda_nm"].values, dfA["I"].values
    lamB, IB = dfB["lambda_nm"].values, dfB["I"].values

    fitA = fit_spectrum_lambda(lamA, IA, model=args.model, T_grid=(args.Tmin,args.Tmax,args.dT))
    fitB = fit_spectrum_lambda(lamB, IB, model=args.model, T_grid=(args.Tmin,args.Tmax,args.dT))

    # crude relative uncertainties proxy
    n = len(IA)
    Tstep = args.dT
    sigma_relA = (Tstep * np.sqrt(fitA["RSS"]/n)) / (fitA["T_best"] * (np.max(IA) + 1e-9))
    nB = len(IB)
    sigma_relB = (Tstep * np.sqrt(fitB["RSS"]/nB)) / (fitB["T_best"] * (np.max(IB) + 1e-9))

    dT_over_T_obs = (fitB["T_best"] - fitA["T_best"]) / fitA["T_best"]
    pred = frac_shift(args.alpha, args.pA, args.chi, args.u_ae) - frac_shift(args.alpha, args.pB, args.chi, args.u_ae)
    sigma_rel = float(np.sqrt(sigma_relA**2 + sigma_relB**2))
    z = float((dT_over_T_obs - pred) / (sigma_rel + 1e-18))

    out = dict(
        model=args.model,
        alpha=args.alpha, pA_Pa=args.pA, pB_Pa=args.pB, chi=args.chi, u_ae_Pa=args.u_ae,
        T_fit_A_K=fitA["T_best"], T_fit_B_K=fitB["T_best"],
        dT_over_T_obs=dT_over_T_obs,
        frac_shift_pred=pred,
        z_score=z,
        note="|z|>2 roughly improbable under (obs - pred) at ~95% CL; compare also to chi=0 baseline."
    )
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
