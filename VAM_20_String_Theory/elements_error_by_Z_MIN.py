#!/usr/bin/env python3
# elements_error_by_Z_MIN.py
# Build abs(% error) vs Z from your SST_Invariant_Mass_Results_all_modes.csv
# Saves PNG+PDF and a small CSV of the plotted data.

import pandas as pd, numpy as np, matplotlib.pyplot as plt, re

CSV = "SST_Invariant_Mass_Results_all_modes.csv"
OUT = "elements_error_by_Z_canonical"

def parse_pct(s):
    if pd.isna(s): return np.nan
    m = re.search(r'([-+]?\d*\.?\d+)\s*%', str(s))
    return float(m.group(1)) if m else np.nan

df = pd.read_csv(CSV)

# Parse the three error columns present in your file
df['err_exact']  = df['% Error'].apply(parse_pct)
df['err_canon']  = df['% Error [CANON]'].apply(parse_pct)
df['err_sector'] = df['% Error [Sector Norm]'].apply(parse_pct)

# Periodic table map (Z=1..103; we only need 1..92 for your run)
symbols = [
    "H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca",
    "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr",
    "Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba",
    "La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu",
    "Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn",
    "Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr"
]
sym2Z = {s:i+1 for i,s in enumerate(symbols)}

# Keep only rows that are elements; attach Z
df['Z'] = df['Object'].map(sym2Z)
el = df[df['Z'].notna()].copy()
el['Z'] = el['Z'].astype(int)

# Best available error per row: CANON > exact > sector
el['abs_pct_error'] = el['err_canon'].abs()
mask = el['abs_pct_error'].isna()
el.loc[mask, 'abs_pct_error'] = el.loc[mask, 'err_exact'].abs()
mask = el['abs_pct_error'].isna()
el.loc[mask, 'abs_pct_error'] = el.loc[mask, 'err_sector'].abs()
el = el.dropna(subset=['abs_pct_error']).sort_values('Z')

# Save the data used
el[['Z','Object','abs_pct_error']].to_csv(f"{OUT}_data.csv", index=False)

# Plot (single figure, default style/colors)
plt.figure()
plt.scatter(el['Z'], el['abs_pct_error'], s=12)
plt.plot(el['Z'], el['abs_pct_error'])
plt.xlabel("Atomic number $Z$")
plt.ylabel("Absolute percent error")
plt.title("Elemental mass error vs $Z$ (prefer CANON; fallback exact/sector)")
plt.tight_layout()
plt.savefig(f"{OUT}.png", dpi=200)
plt.savefig(f"{OUT}.pdf")
plt.close()

# Print quick stats
errs = el['abs_pct_error'].to_numpy()
print(f"Elements included: {len(errs)}")
print(f"Median |% error|: {np.median(errs):.3f}%")
print(f"95th percentile: {np.percentile(errs,95):.3f}%")
print(f"Range: {errs.min():.3f}% .. {errs.max():.3f}%")
