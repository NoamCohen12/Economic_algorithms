from utils import (
    find_assignment,
    build_envy_graph,
    check_envy,
    print_result,
)


def envy_free_room_allocation(
        valuations: list[list[float]],
        rent: float,
        VERBOSE: bool = False,
):
    """
    This function implements the envy-free room allocation algorithm.
    :param VERBOSE:fpr dibuging
    :param valuations:matrix of valuations where each row represents a player and each column represents a room.
    :param rent:how much each player has to pay for the room.
    :return:
    """

    # Create a bipartite graph each player i is connected to row i of the matrix
    # and each edge has weight equal to the value of player i for room j.
    assignment = find_assignment(valuations)
    # find for each player their subvention by the Bellman Ford algorithm
    Graph_Envy = build_envy_graph(valuations, assignment)
    if VERBOSE:
        print(f"Graph_Envy :{Graph_Envy.edges.data()}")

    # find the longest path from the source to all other nodes in the graph G.
    subvention = Bellman_Ford_subvention(Graph_Envy, "P0")
    if VERBOSE:
        print(f"subvention :{subvention}")
    # Calculate the payment for each player.
    payments = Payment(subvention, rent)

    # Print the result of the envy-free room allocation.
    if VERBOSE:
        print_result(valuations, assignment, payments)

    if check_envy(valuations, assignment, payments):
        print("❌ There is envy in the allocation.")
    elif VERBOSE:
        print("✅ The allocation is envy-free.")

    return assignment, payments


def Bellman_Ford_subvention(G, source) -> dict:
    """
    This function finds the longest path from the source to all other nodes in the graph G.
    :param G:graph where each edge has weight equal to the value of player i for room j.
    :param source:the source node.
    :return:
    """
    # Initialization: Minimum distances to -∞, except for the origin
    dist = {node: float('-inf') for node in G.nodes}
    dist[source] = 0

    # over |V|-1 loop
    for _ in range(len(G.nodes) - 1):
        for u, v, data in G.edges(data=True):
            weight = data.get('weight', 0)
            if dist[u] + weight > dist[v]:
                dist[v] = dist[u] + weight

    # check if there is positive cycle
    for u, v, data in G.edges(data=True):
        weight = data.get('weight', 0)
        if dist[u] + weight > dist[v]:
            raise ValueError("there is positive cycle")

    return dist


def Payment(subvention: dict, rent: float) -> dict:
    """
    This function calculates the payment for each player.
    :param subvention:the longest path from the source to all other nodes in the graph G.
    :param rent:how much each player has to pay for the room.
    :return:
    """
    sum_subvention = sum(subvention.values())
    num_players = len(subvention)
    # Calculate the average subvention
    avg_subvention = (sum_subvention - rent) / num_players
    for player in subvention:
        subvention[player] = subvention[player] - avg_subvention

    return subvention


if __name__ == "__main__":
    print("\n--- Case 1 ---")
    envy_free_room_allocation([[150, 0], [140, 10]], rent=100, VERBOSE=True)

    print("\n--- Case 2 ---")
    envy_free_room_allocation([[100, 100], [100, 100]], rent=100, VERBOSE=True)

    print("\n--- Case 3 ---")
    envy_free_room_allocation([[90, 100], [80, 120]], rent=100, VERBOSE=True)

    print("\n--- Case 4 ---")
    envy_free_room_allocation([[100, 0], [50, 50]], rent=100, VERBOSE=True)

    print("\n--- Case 5 ---")
    envy_free_room_allocation([[1000, 10], [5, 990]], rent=100, VERBOSE=True)

    print("\n--- Case 6 ---")
    envy_free_room_allocation([[100, 0, 0], [0, 100, 0], [0, 0, 100]], rent=300, VERBOSE=True)

    print("\n--- Case 7 ---")
    envy_free_room_allocation([[100, 200, 0], [0, 100, 200], [200, 0, 100], ], rent=300, VERBOSE=True)
