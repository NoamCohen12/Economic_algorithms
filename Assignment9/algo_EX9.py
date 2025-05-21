import matplotlib

try:
    # Works well on most desktop environments (Windows / macOS / Linux)
    matplotlib.use("TkAgg")
except ImportError:
    # Fallback for environments without a GUI (e.g., SSH servers, headless systems)
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from typing import List, Tuple


# --------------------------------------------------------------------
#  build bipartite graph
# --------------------------------------------------------------------
def build_bipartite_graph(M: np.ndarray) -> Tuple[nx.Graph, List[str], List[str]]:
    """יוצר גרף דו-צדדי משוקלל (רק משקלים > 0)."""
    n = M.shape[0]
    left = [f"a{i}" for i in range(n)]
    right = [f"b{j}" for j in range(n)]
    G = nx.Graph()
    G.add_nodes_from(left, bipartite=0)
    G.add_nodes_from(right, bipartite=1)

    for i in range(n):
        for j in range(n):
            w = M[i, j]
            if w > 1e-6:
                G.add_edge(left[i], right[j], weight=w)
    return G, left, right


def draw_step(G: nx.Graph,
              pos: dict,
              matching_edges: List[Tuple[str, str]],
              title: str) -> None:
    """
    Draws the graph; matching edges in red, remaining edges in gray.
    """
    # Determine edge colors: red if in matching, otherwise gray
    edge_colors = [
        "firebrick" if {u, v} in [{*e} for e in matching_edges] else "lightgrey"
        for u, v in G.edges()
    ]

    # Determine edge widths: thicker for matching, otherwise scaled by weight
    edge_widths = [
        3.2 if {u, v} in [{*e} for e in matching_edges] else 1.5 + 2 * G[u][v]["weight"]
        for u, v in G.edges()
    ]

    # Create edge labels showing the weight (rounded to 2 decimals)
    edge_labels = {
        e: f"{G[e[0]][e[1]]['weight']:.2f}"
        for e in G.edges()
        if G[e[0]][e[1]]['weight'] > 1e-6  # show only if weight > 0
    }
    fig = plt.figure(figsize=(7, 4))  # Save handle to close later
    nx.draw_networkx_nodes(G, pos, node_color="#BBDEFB", node_size=850)
    nx.draw_networkx_labels(G, pos, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()

    plt.show()  # By default, blocks execution until window is closed
    plt.close(fig)  # Free memory after closing the window


# --------------------------------------------------------------------
# algorithm birkhoff_decomposition
# --------------------------------------------------------------------
def birkhoff_decomposition(M: np.ndarray) -> None:
    table = []
    if np.all(M.sum(axis=0) != 1) or np.all(M.sum(axis=1) != 1):
        raise ValueError("The graph is not balanced:  (rows and columns must each sum to 1")
    n = M.shape[0]

    pos = {}

    """
    i     j
    a1    b1
    a2    b2
    ...   ...
    """
    for i in range(n):
        pos[f"a{i}"] = (0, n - i)

    for j in range(n):
        pos[f"b{j}"] = (2, n - j)

    step = 1
    while M.sum() > 0:
        G, left, right = build_bipartite_graph(M)
        """" matching is a dict of a->b and b->a """
        matching = nx.algorithms.bipartite.maximum_matching(G, top_nodes=left)
        """"matching is a list of a->b without b->a """
        match_edges = [(u, v) for u, v in matching.items() if u in left]
        if len(match_edges) < n:
            print(f"Step {step}: Incomplete matching")
            print("Matching edges:", match_edges)
            print("Matrix M:\n", M)
            raise RuntimeError("num of matches < n , not a perfect matching")

        weights = []
        for u, v in match_edges:
            i = int(u[1:])  # 'a0' → 0
            j = int(v[1:])  # 'b2' → 2
            weights.append(M[i, j])

        min_weights = min(weights)
        table.append((round(min_weights, 6), match_edges))
        # print(min_weights)

        draw_step(G, pos, match_edges,
                  f"Step {step}: Perfect matching and reduce = {min_weights:.2f}")

        # reduce min_edge_in_match from all edges in the matching
        for u, v in match_edges:
            i, j = int(u[1:]), int(v[1:])
            M[i, j] -= min_weights  # don't use max(..., 0.0)

        # CLEANUP: eliminate numerical noise
        M[M < 1e-8] = 0.0

        # new graph after reduction
        G_after_reduce, _, _ = build_bipartite_graph(M)
        draw_step(G_after_reduce, pos, [], f"Step {step}: Graph after reduction (total weight = {M.sum():.2f})")
        step += 1
    return table


def print_matching_table(table: List[Tuple[float, List[Tuple[str, str]]]]):
    print("Final decomposition:\n")
    for prob, match_edges in table:
        pairs_str = " , ".join(f"{u}--{v}" for u, v in match_edges)
        print(f"• With probability {prob:.1f}: {pairs_str}")


if __name__ == "__main__":
    test_matrices = [
        ("example in class", np.array([
            [0.0, 0.0, 0.3, 0.7],
            [0.3, 0.7, 0.0, 0.0],
            [0.4, 0.3, 0.0, 0.3],
            [0.3, 0.0, 0.7, 0.0],
        ])),
        ("original", np.array([
            [0.0, 0.5, 0.5, 0.0],
            [0.4, 0.3, 0.0, 0.3],
            [0.2, 0.2, 0.5, 0.1],
            [0.4, 0.0, 0.0, 0.6],
        ])),
        ("Identity", np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ])),
        ("Uniform 3x3", np.array([
            [1 / 3, 1 / 3, 1 / 3],
            [1 / 3, 1 / 3, 1 / 3],
            [1 / 3, 1 / 3, 1 / 3]
        ])),
        ("Two matchings", np.array([
            [0.5, 0.5, 0.0],
            [0.0, 0.5, 0.5],
            [0.5, 0.0, 0.5]
        ])),
        ("error", np.array([
            [0.2, 0.8],
            [0.2, 0.2]
        ]))

    ]

    for name, matrix in test_matrices:
        print(f"\n=== Test: {name} ===")
        print("Matrix M:\n", matrix)
        table = birkhoff_decomposition(matrix.copy())
        print_matching_table(table)
