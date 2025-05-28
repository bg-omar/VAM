import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Ensure it uses Tkinter backend

# Gegevens: Elementen en corresponderende torusknopen
elementen = [
    "Waterstof", "Helium", "Lithium", "Beryllium", "Boor", "Koolstof", "IJzer", "Uranium"
]
Z = [1, 2, 3, 4, 5, 6, 26, 92]  # Atoomnummers
knopen = ["T(2,3)", "T(2,5)", "T(2,7)", "T(2,9)", "T(2,11)", "T(2,13)", "T(4,3)", "Complex / Samengesteld"]
helicitiet = [3, 5, 7, 9, 11, 13, 8, None]

# Maak DataFrame
df_knopen = pd.DataFrame({
    "Element": elementen,
    "Z": Z,
    "TorusKnoop": knopen,
    "Heliciteit $L_k$": helicitiet
})
# Corrigeer heliciteit door uranium expliciet een zichtbare dummywaarde te geven
df_corr = df_knopen.copy()
df_corr.loc[df_corr["Element"] == "Uranium", "Heliciteit $L_k$"] = 1  # zichtbaar maken

# Kleurenschema met laatste balk anders
bar_colors = ["cornflowerblue"] * (len(df_corr) - 1) + ["dimgray"]
bar_heights = df_corr["Heliciteit $L_k$"].astype(float).tolist()

# Plot met geforceerde uraniumbalk
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df_corr["Element"], bar_heights, color=bar_colors, edgecolor="black")

for bar, label, element in zip(bars, df_corr["TorusKnoop"], df_corr["Element"]):
    height = bar.get_height()
    if element != "Uranium":
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, label,
                ha='center', va='bottom', fontsize=9)
    else:
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5,
                "Samengesteld", ha='center', va='bottom',
                fontsize=9, style='italic', color='black')

# Afwerking
ax.set_ylabel("Heliciteit $L_k$")
ax.set_title("Elementen als Torusknopen binnen het Vortex Æther Model")
ax.set_ylim(0, 15)
plt.xticks(rotation=45)


# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.pdf"
plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()

# Diagram 3: Energetisch voordeel bij splitsing vs fusie

# Stel een hypothetisch verband op tussen heliciteit en energie
Lk_values = np.arange(1, 21)  # heliciteit van 1 tot 20
E_single = Lk_values**2       # energie als enkele knoop ~ Lk^2
E_split = (Lk_values // 2)**2 + (Lk_values - Lk_values // 2)**2  # splitsing in twee knopen

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(Lk_values, E_single, label="Eén knoop", color='royalblue', linewidth=2)
ax.plot(Lk_values, E_split, label="Twee gesplitste knopen", color='darkorange', linestyle='--', linewidth=2)

# Annotatie van verschil
diff = E_single - E_split
max_idx = np.argmax(diff)
ax.annotate("Maximaal energetisch voordeel\nbij splitsing",
            xy=(Lk_values[max_idx], E_split[max_idx]),
            xytext=(Lk_values[max_idx]+1, E_split[max_idx]+80),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=10, color='black')

# Afwerking
ax.set_xlabel("Totale heliciteit $L_k$")
ax.set_ylabel("Vortexenergie $E$")
ax.set_title("Energetisch voordeel bij knoopsplitsing vs. fusie")
ax.legend()
ax.grid(True)


# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"3_EnergetischVoordeel.pdf"
plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"3_EnergetischVoordeel.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()

# Diagram 4: Periodiciteit als functie van knoopfamilies

# Hypothetische knoopfamilies: p=2,3,4,5,6
knoopfamilies = {
    2: {"begin_Z": 1, "count": 2},   # H, He
    3: {"begin_Z": 3, "count": 8},   # Li - Ne
    4: {"begin_Z": 11, "count": 18}, # Na - Ar
    5: {"begin_Z": 29, "count": 18}, # Cu - Kr
    6: {"begin_Z": 47, "count": 32}  # Cs - Rn
}

# Zet data om in lijsten
families = []
Z_ranges = []
counts = []
for p, data in knoopfamilies.items():
    families.append(f"p={p}")
    Z_ranges.append(f"{data['begin_Z']}–{data['begin_Z'] + data['count'] - 1}")
    counts.append(data['count'])

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(families, counts, color="mediumseagreen", edgecolor="black")

# Annotaties
for bar, zrange in zip(bars, Z_ranges):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1, f"Z={zrange}", ha='center', fontsize=9)

# Stijl
ax.set_ylabel("Aantal elementen")
ax.set_title("Periodieke reeksen als knoopfamilies in VAM ($p$-waarden)")
ax.set_ylim(0, 40)
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"4_KnoopFamilies.pdf"
plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"4_KnoopFamilies.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()

# Diagram 5: Wervelveldenergie versus heliciteit

# Helicitywaarden en energieberekeningen
Lk_range = np.linspace(1, 20, 200)
E_linear = Lk_range           # lineair verband (klassiek model)
E_quadratic = Lk_range**2     # VAM: energie ~ Lk^2
E_log = Lk_range * np.log(Lk_range)  # alternatieve schaal voor lichte knopen

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(Lk_range, E_linear, label="Lineair: $E \\propto L_k$", linestyle='--', color='gray')
ax.plot(Lk_range, E_quadratic, label="VAM: $E \\propto L_k^2$", color='crimson', linewidth=2)
ax.plot(Lk_range, E_log, label="Log-versterkt: $E \\propto L_k \\log L_k$", linestyle=':', color='blue')

# Labels
ax.set_xlabel("Heliciteit $L_k$")
ax.set_ylabel("Vortexenergie $E$")
ax.set_title("Vergelijking van energiemodellen voor vortexknopen")
ax.legend()
ax.grid(True)
# ✅ Get the script filename dynamically and save as pdf
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"5_Wervelveldenergie.pdf"
plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"5_Wervelveldenergie.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()