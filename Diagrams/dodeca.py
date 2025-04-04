import numpy as np
import matplotlib.pyplot as plt

# Define atomic radii (in pm)
elements = ["Hydrogen", "Helium", "Carbon"]
atomic_radii = np.array([53, 31, 70])  # in pm

# Compute pentagonal face diameters
d_dodecahedron = 0.577 * atomic_radii
d_icosahedron = 0.632 * atomic_radii

# Observed spectral emission wavelengths (in nm)
observed_wavelengths = {
    "Hydrogen": [410, 434, 486, 656],
    "Helium": [388, 447, 468, 501],
    "Carbon": [426, 493, 567, 658],
}

# Expected wavelengths from dodecahedron and icosahedron (converted to nm)
expected_wavelengths_dodecahedron = d_dodecahedron * 10  # Convert pm to nm
expected_wavelengths_icosahedron = d_icosahedron * 10  # Convert pm to nm

# Plot results
fig, ax = plt.subplots(figsize=(8, 6))

for i, element in enumerate(elements):
    ax.scatter(
        [element] * len(observed_wavelengths[element]),
        observed_wavelengths[element],
        color="blue",
        label="Observed Emission" if i == 0 else "",
        marker="o",
        )
    ax.scatter(
        element,
        expected_wavelengths_dodecahedron[i],
        color="red",
        label="Dodecahedron Prediction" if i == 0 else "",
        marker="s",
    )
    ax.scatter(
        element,
        expected_wavelengths_icosahedron[i],
        color="green",
        label="Icosahedron Prediction" if i == 0 else "",
        marker="^",
    )

# Labels and legend
ax.set_ylabel("Wavelength (nm)")
ax.set_title("Comparison of Predicted and Observed Atomic Spectra")
ax.legend()
ax.grid(True)

# Show plot
plt.show()