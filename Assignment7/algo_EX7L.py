import networkx as nx
import cvxpy as cp
from utils import (
    find_assignment,
    build_envy_graph,
    check_envy,
    print_result,
)


def envy_free_room_allocation_L(
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

    payments = compute_payments_cvxpy(valuations, assignment, rent)

    # Print the result of the envy-free room allocation.
    if VERBOSE:
        print_result(valuations, assignment, payments)

    if check_envy(valuations, assignment, payments):
        print("❌ There is envy in the allocation.")
    elif VERBOSE:
        print("✅ The allocation is envy-free.")

    return assignment, payments


def compute_payments_cvxpy(valuations: list[list[float]], assignment: list[int], rent: float) -> dict:
    n = len(valuations)
    p = cp.Variable(n)

    constraints = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            lhs = valuations[i][assignment[i]] - p[i]
            rhs = valuations[i][assignment[j]] - p[j]
            constraints.append(lhs >= rhs)

    constraints.append(cp.sum(p) == rent)

    prob = cp.Problem(cp.Minimize(0), constraints)
    prob.solve()

    if prob.status != cp.OPTIMAL:
        raise ValueError("No envy-free payments found")

    return {f"P{i}": p.value[i] for i in range(n)}


if __name__ == "__main__":
    print("\n--- Case 1 ---")
    envy_free_room_allocation_L([[150, 0], [140, 10]], rent=100, VERBOSE=True)

    print("\n--- Case 2 ---")
    envy_free_room_allocation_L([[100, 100], [100, 100]], rent=100, VERBOSE=True)

    print("\n--- Case 3 ---")
    envy_free_room_allocation_L([[90, 100], [80, 120]], rent=100, VERBOSE=True)

    print("\n--- Case 4 ---")
    envy_free_room_allocation_L([[100, 0], [50, 50]], rent=100, VERBOSE=True)

    print("\n--- Case 5 ---")
    envy_free_room_allocation_L([[1000, 10], [5, 990]], rent=100, VERBOSE=True)

    print("\n--- Case 6 ---")
    envy_free_room_allocation_L([[100, 0, 0], [0, 100, 0], [0, 0, 100]], rent=300, VERBOSE=True)

    print("\n--- Case 7 ---")
    envy_free_room_allocation_L([[100, 200, 0], [0, 100, 200], [200, 0, 100], ], rent=300, VERBOSE=True)
