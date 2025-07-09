# 🌀 Vortex Æther Model (VAM)

Welcome to the theoretical fringes.

This repository hosts a collection of exploratory papers, simulations, and visualizations centered around the **Vortex Æther Model (VAM)** — a fluid-dynamical reinterpretation of gravity, time dilation, and quantum phenomena. VAM posits that all fundamental interactions emerge from variations in a universal, superfluid-like æther, driven by topological vortex structures.

> Because if spacetime can curve, why can’t it swirl?

---

## 📚 Projects

This repository includes the following key documents:

- **Time Dilation in 3D Superfluid Æther Model**  
  A reinterpretation of relativistic time dilation via swirl-induced clock slowdown.

- **Swirl Clocks and Vorticity-Induced Gravity**  
  Proposes an alternative mechanism for gravity based on Bernoulli-like pressure gradients in rotating æther.

- **Benchmarking Vortex Æther Model vs General Relativity**  
  Numerical tests comparing VAM predictions with known GR results in extreme scenarios. 

- **Standard Model Lagrangian in VAM**  
  A bold attempt to reconstruct quantum field theory from first principles using vortex topologies.

---

## License

This repository is licensed under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) license.  
© 2025 Omar Iskandarani. Use for educational and research purposes only. Commercial reuse prohibited without permission.


## 📈 Zenodo-Registered Releases

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15566101.svg)](https://doi.org/10.5281/zenodo.15566101)  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15566319.svg)](https://doi.org/10.5281/zenodo.15566319)  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15566336.svg)](https://doi.org/10.5281/zenodo.15566336)

All papers and associated code are archived on [Zenodo](https://zenodo.org/) for permanent accessibility and citation.

---

## 🔬 Author

**ORCID**: [0009-0006-1686-3961](https://orcid.org/0009-0006-1686-3961)  
Conceived, written,  and fearlessly launched into the æther by a person undeterred by the collapse of academic consensus.

---

## 🧠 Topics of Interest

- General Relativity vs Fluid Models
- Æther Theory Redux (with turbulence)
- Superfluid Analog Gravity
- Quantum Topology in Continuum Mechanics
- Gravitational Redshift without Geometry
- Time Dilation via Vortex Clock Models
- Casimir, Entanglement, Tunneling: Fluid-Style

---

## 🛠️ Simulations & Plots

Visual tools (coming soon) for:
- Comparing VAM and GR time dilation near compact objects
- Simulating æther inflow velocities and pressure gradients
- Visualizing vortex-induced lensing and frame-dragging

> Because if you can’t visualize your theory, is it even real?

## 📝 Equation Extraction

Run the helper script to harvest equations from each VAM paper and convert them
into Python-friendly expressions.  `VAM - 2 Swirl Clocks` was processed first,
and running the tool again will generate JSON files for the other folders
(including the English translation in `VAM - 1 TimeDilation/TimeDilation`):

```bash
python tools/extract_equations.py
```

The Swirl Clocks equations are stored in `out/extracted_equations.json`.  All
other VAM directories produce their own JSON files inside `out/equations/`, with
names derived from the directory titles (spaces replaced with underscores).
These files can be imported in tests or further analysis.

---

## ⚠️ Disclaimer

This project may cause mild academic rage, spontaneous fluid metaphors, or a strong desire to challenge Einstein to a swirl-off. Reader discretion is advised.

---

## 📬 Feedback

Open an issue, fork the repo, or send your complaints directly into the æther. It’s listening. Always.