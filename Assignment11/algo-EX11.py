import cvxpy as cp
import numpy as np
import pandas as pd


def find_decomposition(budget: list[float], preferences: list[set[int]]):
    """
    Find a decomposition of the budget into sets of candidates that can be supported by the voters.
    and return the decomposition
    """
    C = sum(budget)  # Total budget
    n = len(preferences)  # Number of citizen
    m = len(budget)  # Number of candidates

    matrix = cp.Variable((n, m))  # matrix of how many citizen pay of each candidate

    constraints = []

    # Constraint sum of all raw is C/n
    constraints.append(cp.sum(matrix, axis=1) == C / n)

    # Constraint sum column[i] is budget[i]
    for j in range(m):
        constraints.append(cp.sum(matrix[:, j]) == budget[j])

    # Constraint if citizen i not prefer candidate j, then matrix[i, j] == 0
    # not B -> not A
    for i in range(n):
        for j in range(m):
            if j not in preferences[i]:
                constraints.append(matrix[i, j] == 0)

    # Constraint matrix[i, j] >= 0 for all i, j
    constraints.append(matrix >= 0)

    problem = cp.Problem(cp.Minimize(0), constraints)
    problem.solve()

    if problem.status == 'optimal':
        solution = matrix.value.round(2)
        print("found a legal allocation:")
        return solution
    else:
        raise ValueError("No legal allocation found. Problem status: " + problem.status)


def print_allocation_table(matrix: np.ndarray):
    """
    Receives an allocation matrix of shape [citizens × topics]
    and prints it in a nicely formatted table.
    """
    n, m = matrix.shape

    # Clean near-zero values (e.g., -0.0 or 1e-10)
    matrix[np.abs(matrix) < 1e-6] = 0

    # Create labeled DataFrame
    df = pd.DataFrame(
        data=matrix,
        index=[f"Citizen {i}" for i in range(n)],
        columns=[f"Topic {j}" for j in range(m)]
    )

    print("\n📊 Allocation Table:")
    print(df.to_string(float_format=lambda x: f"{x:6.2f}"))


if __name__ == "__main__":
    print("\n--- Case 1 ---")
    budget1 = [400, 50, 50, 0]
    preferences1 = [{0, 1}, {0, 2}, {0, 3}, {1, 2}, {0}]
    matrix1 = find_decomposition(budget1, preferences1)
    print_allocation_table(matrix1)

    print("\n--- Case 2 ---")
    budget2 = [250, 250, 100]
    preferences2 = [{0}, {1}, {2}]
    matrix2 = find_decomposition(budget2, preferences2)
    print_allocation_table(matrix2)

