import matplotlib.pyplot as plt
import networkx as nx

# Improve layout: use a layered approach with clearer flow and vertical spacing
# Use simpler positions and a cleaner diagram with improved labels

# Create a new directed graph
G2 = nx.DiGraph()

# Define edges for the flow
G2.add_edges_from([
    ("Einstein's late æther", "Structured Space"),
    ("Structured Space", "VAM Concepts"),
    ("Einstein's late æther", "Vorticity"),
    ("Vorticity", "Time"),
    ("Vorticity", "Gravity")
])

# Define new positions for better clarity in a top-down hierarchy
pos2 = {
    "Einstein's late æther": (0, 3),
    "Structured Space": (0, 2),
    "VAM Concepts": (0, 1),
    "Vorticity": (2, 2.5),
    "Time": (3, 1.5),
    "Gravity": (1, 1.5)
}

# Draw updated diagram
plt.figure(figsize=(10, 6))
nx.draw_networkx_nodes(G2, pos2, node_color='lightyellow', node_size=2500, edgecolors='black')
nx.draw_networkx_edges(G2, pos2, arrowstyle='-|>', arrowsize=20, edge_color='black', width=2)
nx.draw_networkx_labels(G2, pos2, font_size=11, font_family='sans-serif')

plt.title("Einstein’s Æther → Structured Space → VAM Concepts", fontsize=14, pad=20)
plt.axis('off')
plt.tight_layout()
import os
script_name = os.path.splitext(os.path.basename(__file__))[0]
filename = f"{script_name}.pdf"
plt.savefig(filename, format="pdf", bbox_inches="tight")
filename = f"{script_name}.png"
plt.savefig(filename, dpi=150)  # Save image with high resolution
plt.tight_layout()
plt.show()

