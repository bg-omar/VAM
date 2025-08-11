#!/usr/bin/env python3
import pandas as pd
import numpy as np

# Prefactors (kg per meter) computed from your constants:
K_fluid = 9.844625550645777684e-39
K_energy = 8.226091068037216298e-09

def choose_H(row):
    # Priority: use Hvortex_Vol if hyperbolic_volume present, else Hvortex_Lk for links, else Hvortex_X
    try:
        sigma = float(row.get("sigma", 0) or 0)
    except:
        sigma = 0.0
    # If sigma is 0 (amphichiral), all charges are zero by rule
    if sigma == 0:
        return 0.0
    # Volume-based
    vol = row.get("hyperbolic_volume", "")
    vbase = row.get("volume_baseline_value", "")
    if vol not in ["", None] and vbase not in ["", None]:
        try:
            vol = float(vol); vbase = float(vbase)
            if vbase != 0:
                return sigma * (vol / vbase)
        except:
            pass
    # Link-based
    if str(row.get("type","")).lower() == "link":
        lk = row.get("sum_abs_linkings", "")
        try:
            lk = float(lk)
            return sigma * lk
        except:
            pass
    # Crossing-based
    cr = row.get("crossing_number", "")
    b0 = row.get("base_offset_b0", 3)
    try:
        cr = float(cr); b0 = float(b0)
        return sigma * max(cr - b0, 0.0)
    except:
        return 0.0

def main(in_path, out_path):
    df = pd.read_csv(in_path)
    Hvals = []
    Mfluid = []
    Menergy = []
    for _, row in df.iterrows():
        H = choose_H(row)
        Hvals.append(H)
        try:
            xi = float(row.get("xi", 1.0))
        except:
            xi = 1.0
        try:
            L = float(row.get("L_knot_m", 0.0))
        except:
            L = 0.0
        Mfluid.append(xi * H * K_fluid * L)
        Menergy.append(xi * H * K_energy * L)
    # If Hvortex_* columns are present, we do not overwrite; we add a derived column
    df["H_vortex_DERIVED"] = Hvals
    df["mass_fluid_kg_DERIVED"] = Mfluid
    df["mass_energy_kg_DERIVED"] = Menergy
    df.to_csv(out_path, index=False)
    print("Wrote:", out_path)
    print("Note: K_fluid = {:.6e} kg/m, K_energy = {:.6e} kg/m".format(9.844626e-39, 8.226091e-09))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: compute_Hvortex_and_mass.py INPUT.csv OUTPUT.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
