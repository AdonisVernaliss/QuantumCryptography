# visualize_qkd_full_mesh.py

import matplotlib.pyplot as plt
import networkx as nx
from DFMQKDS import get_node_names, exchange_key_length, generate_qubits, process_qubits, extract_key
from itertools import combinations


def visualize_full_mesh_network(num_nodes):
    # Set up the nodes and connections for a full mesh
    nodes = get_node_names(num_nodes)
    connections = list(combinations(nodes, 2))

    # Set key length and initialize data structures
    key_length = exchange_key_length()
    node_qubit_data = {}
    keys = {}

    # Prepare data for each node's qubits
    for node in nodes:
        qubits = generate_qubits(key_length)
        processed_qubits = process_qubits(qubits)
        node_qubit_data[node] = {
            "angles": [q[0] for q in qubits],
            "states": [q[1] for q in qubits],
            "processed": processed_qubits
        }

    # Calculate keys between each pair in the full mesh
    for p1, p2 in connections:
        key = extract_key(node_qubit_data[p1]["processed"], node_qubit_data[p2]["processed"])
        keys[(p1, p2)] = key

    # Set up the full mesh network using NetworkX
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(connections)

    # Position nodes in a circular layout for full mesh visualization
    pos = nx.circular_layout(G)

    # Draw the graph
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="skyblue")
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold", font_color="black")

    # Annotate each node with their qubit states for visualization
    for node, data in node_qubit_data.items():
        x, y = pos[node]
        plt.text(
            x, y - 0.15, f"Angles: {data['angles']}\nStates: {data['states']}",
            ha='center', fontsize=8, bbox=dict(facecolor='white', alpha=0.5)
        )

    # Add key values as labels for each edge
    for (p1, p2), key in keys.items():
        # Find midpoint between nodes for placing the key
        (x1, y1), (x2, y2) = pos[p1], pos[p2]
        x_mid, y_mid = (x1 + x2) / 2, (y1 + y2) / 2
        plt.text(
            x_mid, y_mid, f"Key: {key}", ha='center', fontsize=9, color="red",
            bbox=dict(facecolor='white', alpha=0.7)
        )

    plt.title("Full Mesh QKD Network with Node States and Keys")
    plt.show()


# Main function to execute the visualization
if __name__ == "__main__":
    num_nodes = int(input("Enter the number of nodes in the full mesh network: "))
    visualize_full_mesh_network(num_nodes)
