# 🌀 Vortex Æther Model (VAM)

Welcome to the theoretical fringes.

This repository hosts a collection of exploratory papers, simulations, and visualizations centered around the **Vortex Æther Model (VAM)** — a fluid-dynamical reinterpretation of gravity, time dilation, and quantum phenomena. VAM posits that all fundamental interactions emerge from variations in a universal, superfluid-like æther, driven by topological vortex structures.

> Because if spacetime can curve, why can’t it swirl?

---

## 📖 Papers and Simulation Projects
This repository contains a series of papers and simulation projects that explore the Vortex Æther Model, its implications for gravity, time dilation, and quantum mechanics, and how it contrasts with traditional spacetime theories. Each paper builds on the previous work, creating a comprehensive framework that challenges established paradigms. DOI are shown for each release.


- **Einstein and the Æther (Opening Paper)**  
  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15669901.svg)](https://doi.org/10.5281/zenodo.15669901)  

- **Time Dilation in 3D Superfluid Æther Model (Opening Paper)**  
  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15669794.svg)](https://doi.org/10.5281/zenodo.15669794)
  
- **Swirl Clocks and Vorticity-Induced Gravity**  
  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15566335.svg)](https://doi.org/10.5281/zenodo.15566335)

- **Benchmarking Vortex Æther Model vs General Relativity**  
  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15665432.svg)](https://doi.org/10.5281/zenodo.15665432)

- **Emergent General Relativity from Structured Swirl Dynamics in VAM**  
  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15712577.svg)](https://doi.org/10.5281/zenodo.15712577)

- **Beyond Spacetime: Gravity, Time, and Vorticity**  
  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15706546.svg)](https://doi.org/10.5281/zenodo.15706546)

- **From Quantum Constants to Galactic Swirl**  
  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15750582.svg)](https://doi.org/10.5281/zenodo.15750582)

- **Knotted Gauge Fields: Rebuilding the Standard Model from Vortex Æther Dynamics**  
 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15772832.svg)](https://doi.org/10.5281/zenodo.15772832)

- **On a Vortex-Based Lagrangian Unification of Gravity and Electromagnetism**  

- **Master Paper – Vortex Æther Framework Summary**  

#### Each paper contributes to the broader theoretical framework of VAM, exploring how fluid dynamics and topological vortices redefine gravity, time, and quantum structure.

## 📈 Zenodo-Registered Releases

- Experimental Validation of the Vortex-Core Tangential Velocity 𝐶𝑒  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15684872.svg)](https://doi.org/10.5281/zenodo.15684872)   
- Experimental Proposal: Gravitational Modulation via Resonant Vortex Structures in Æther  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15692508.svg)](https://doi.org/10.5281/zenodo.15692508)

All papers and associated code are archived on [Zenodo](https://zenodo.org/) for permanent accessibility and citation.


---
## ⚙️ High-Performance Vortex Engine

This repository includes a custom-built Python-to-C++ binding for accelerating Biot–Savart-based vortex interactions.  
Key features:

- 🔁 100x faster evaluation of vortex loops and filaments vs pure Python
- 📦 Seamless Python interface via `pybind11`
- 🧮 Supports time dilation, swirl potential, and local vorticity field extractions
- 🧪 Used to benchmark vortex-based gravitational analogues in the `VAM` model

[High-Performance Vortex Engine](VAMpyBindings/README.md)


---

## License

This repository is licensed under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) license.  
© 2025 Omar Iskandarani. Use for educational and research purposes only. Commercial reuse prohibited without permission.


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