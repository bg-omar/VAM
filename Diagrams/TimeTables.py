# Re-import necessary libraries after kernel reset
import pandas as pd

# Re-create the Temporal Ontology Table
temporal_ontology = pd.DataFrame([
    {
        "Name": "Chronos-time",
        "Symbol": r"$\tau$",
        "Type": "Relative / Measurable",
        "Units": "s (seconds)",
        "Role": "Proper time in localized motion; used in time dilation.",
        "Analogy": "Watch time / Relativity clock"
    },
    {
        "Name": "Aithēr-time",
        "Symbol": r"$\mathcal{N}$",
        "Type": "Absolute / Universal",
        "Units": "s (idealized)",
        "Role": "Universal present; background reference for all temporal flow.",
        "Analogy": "Æther clock / Absolute time"
    },
    {
        "Name": "Swirl Clock",
        "Symbol": r"$\circlearrowleft$ or $S(t)$",
        "Type": "Local / Cyclical",
        "Units": "Phase, radians",
        "Role": "Tracks vortex identity and internal time evolution.",
        "Analogy": "Vortex heartbeat / Phase wheel"
    },
    {
        "Name": "Kairos Moment",
        "Symbol": r"$\mathbb{K}$",
        "Type": "Threshold / Emergent",
        "Units": "Trigger function",
        "Role": "Marks critical topological phase transition or collapse.",
        "Analogy": "Turning point / Collapse event"
    },
    {
        "Name": "Æther Frame",
        "Symbol": r"$\Xi_0$",
        "Type": "Reference Frame",
        "Units": "N/A",
        "Role": "Ideal rest frame of æther; baseline for causality.",
        "Analogy": "Galilean observer / Inertial æther"
    },
    {
        "Name": "Vortex Proper Time",
        "Symbol": r"$T_v$",
        "Type": "Derived / Topological",
        "Units": "s",
        "Role": "Internal geodesic time loop; vortex-specific phase.",
        "Analogy": "Knot-clock / Twist evolution"
    },
    {
        "Name": "Now-Point",
        "Symbol": r"$\nu_0$",
        "Type": "Local Event / Temporal Slice",
        "Units": "Event tag",
        "Role": "Spacetime intersection with the absolute present.",
        "Analogy": "Instantaneous ‘now’ / Ontological cut"
    }
])

import ace_tools_open as tools; tools.display_dataframe_to_user(name="Temporal Ontology Table (VAM)", dataframe=temporal_ontology)