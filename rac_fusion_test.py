import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
import time

# === Setup RAC Nodes in 3D ===
node_positions = {
    "N0": (0, 0, 0), "N1": (1, 0, 0), "N2": (0, 1, 0), "N3": (1, 1, 0), "N4": (0.5, 0.5, 0),
    "N5": (0, 0, 1), "N6": (1, 0, 1), "N7": (0, 1, 1), "N8": (1, 1, 1), "N9": (0.5, 0.5, 1)
}

connections = []

# Create connections between all node pairs within max distance
def build_connections():
    max_dist = 1.1
    nodes = list(node_positions.items())
    for i, (n1, p1) in enumerate(nodes):
        for j, (n2, p2) in enumerate(nodes):
            if i >= j: continue
            dist = np.linalg.norm(np.array(p1) - np.array(p2))
            if dist <= max_dist:
                connections.append((n1, n2))

# === Visualization ===
def draw_rac_grid(active_node=None):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("3D RAC Lattice with BandGap Connections")

    # Draw nodes
    for node, (x, y, z) in node_positions.items():
        color = "red" if node == active_node else "skyblue"
        ax.scatter(x, y, z, s=400, color=color, edgecolors='k')
        ax.text(x, y, z + 0.1, node, fontsize=10, ha='center')

    # Draw bandgap connections
    for n1, n2 in connections:
        x_vals = [node_positions[n1][0], node_positions[n2][0]]
        y_vals = [node_positions[n1][1], node_positions[n2][1]]
        z_vals = [node_positions[n1][2], node_positions[n2][2]]
        ax.plot(x_vals, y_vals, z_vals, color='gray', linewidth=1, alpha=0.5)

    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_zlim(-0.2, 1.2)
    ax.set_axis_off()
    plt.show()

# === Simulate Signal Hopping Across Nodes ===
def simulate_signal_hop(frames=15, delay=0.6):
    visited = []
    current = random.choice(list(node_positions.keys()))
    for _ in range(frames):
        draw_rac_grid(active_node=current)
        neighbors = [n2 for (n1, n2) in connections if n1 == current] + \
                    [n1 for (n1, n2) in connections if n2 == current]
        neighbors = [n for n in neighbors if n not in visited]
        if neighbors:
            visited.append(current)
            current = random.choice(neighbors)
        else:
            current = random.choice(list(node_positions.keys()))
        time.sleep(delay)

# === MAIN RUN ===
build_connections()
simulate_signal_hop()

