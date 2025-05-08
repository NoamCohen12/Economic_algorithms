from __future__ import annotations

from typing import List, Dict

import networkx as nx


# ---------------------------------------------------------------------------
#  matching helper -----------------------------------------------------------
# ---------------------------------------------------------------------------

def find_assignment(valuations: List[List[float]]) -> List[int]:
    """
       This function finds an assignment of rooms to players that is maximum of values.
       :param valuations:matrix of valuations where each row represents a player and each column represents a room.
       :return assignment:dift of assignment:
       """
    n = len(valuations)
    G = nx.Graph()

    players = [f"P{i}" for i in range(n)]
    rooms = [f"R{j}" for j in range(n)]
    G.add_nodes_from(players, bipartite=0)
    G.add_nodes_from(rooms, bipartite=1)

    for i in range(n):
        for j in range(n):
            G.add_edge(players[i], rooms[j], weight=valuations[i][j])

    matching = nx.algorithms.matching.max_weight_matching(G, maxcardinality=True)

    assignment = [-1] * n
    for u, v in matching:
        if u.startswith("P"):
            player, room = int(u[1:]), int(v[1:])
        else:
            player, room = int(v[1:]), int(u[1:])
        assignment[player] = room

    return assignment


# ---------------------------------------------------------------------------
#  envy graph ----------------------------------------------------------------
# ---------------------------------------------------------------------------

def build_envy_graph(valuations: List[List[float]], assignment: List[int]) -> nx.DiGraph:
    """
    create graph that represents the envy of each player towards others.
    E(i,j)=Vi(Xj)−Vi(Xi)
    V(i) is the valuation of player i

    """
    G = nx.DiGraph()
    n = len(valuations)
    for i in range(n):
        G.add_node(f"P{i}")

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            envy = valuations[i][assignment[j]] - valuations[i][assignment[i]]
            G.add_edge(f"P{i}", f"P{j}", weight=envy)
    return G


# ---------------------------------------------------------------------------
#  envy checker --------------------------------------------------------------
# ---------------------------------------------------------------------------

def check_envy(valuations: list[list[float]], assignment: list[int], payments: dict, eps: float = 1e-9) -> bool:
    """
    Returns True if there is envy, i.e., some player prefers another's allocation over their own.
    """
    n = len(valuations)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            my_room = assignment[i]
            their_room = assignment[j]
            my_utility = valuations[i][my_room] - payments[f"P{i}"]
            their_utility = valuations[i][their_room] - payments[f"P{j}"]
            if their_utility > my_utility + eps:
                print(f"Player {i} envies Player {j}: {their_utility} > {my_utility}")
                return True
    return False


# ---------------------------------------------------------------------------
#  nice printing -------------------------------------------------------------
# ---------------------------------------------------------------------------

def print_result(
        valuations: List[List[float]],
        assignment: List[int],
        payments: Dict[str, float],
):
    """
        This function prints the result of the envy-free room allocation.
        """
    for i, room in enumerate(assignment):
        value = valuations[i][room]
        pay = payments[f"P{i}"]
        print(f"Player {i}  ->  room {room:2d}   value = {value:6.1f}   pay = {pay: .2f}")
