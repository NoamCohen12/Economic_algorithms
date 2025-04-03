import cvxpy as cp
import numpy as np


def Egalitarian_division(valuation_matrix: list[list]):
    valuation_matrix = np.array(valuation_matrix)
    if np.any(valuation_matrix < 0):
        raise ValueError("Error: All values in the valuation matrix must be non-negative.")

    n, m = valuation_matrix.shape
    # allocation_matrix-matrix of  how much of each resource is allocated to each agent
    allocation_matrix = cp.Variable((n, m), nonneg=True)
    constraints = []

    # Each resource is fully distributed
    for j in range(m):
        constraints.append(cp.sum(allocation_matrix[:, j]) == 1)

    # utilities of everyone
    utilities = cp.sum(cp.multiply(allocation_matrix, valuation_matrix), axis=1)

    # min Vi(Xi)
    min_utility = cp.Variable()
    for i in range(n):
        constraints.append(min_utility <= utilities[i])

    # max min Vi(Xi)
    objective = cp.Maximize(min_utility)

    problem = cp.Problem(objective, constraints)
    problem.solve()

    if problem.status != "optimal":
        print(f"Warning: Problem could not be solved optimally. Status: {problem.status}")
        return None

    allocation = allocation_matrix.value
    result = {
        "status": problem.status,
        "optimal_value": problem.value,
        "allocation": {},
        "utilities": {}
    }

    for i in range(n):
        result["allocation"][i + 1] = allocation[i].tolist()
        result["utilities"][i + 1] = float(utilities[i].value)

    return result


def print_Div(result, matrix):
    print("\nValuation matrix:")
    for row in matrix:
        print(row)
    print("\nResource allocation:")
    for agent, resources in result["allocation"].items():
        resources_str = ", ".join(
            [f"{value:.2f} of resource #{idx + 1}" for idx, value in enumerate(resources)])
        if resources_str:
            print(f"agent #{agent} get {resources_str}")
        else:
            print(f"agent #{agent} Not getting anything")

    print("\nUtilities:")
    for agent, utility in result["utilities"].items():
        print(f"agent #{agent} has utility {utility:.2f}")


def test_egalitarian_division():
    # Test Case 1: Original matrix
    print("----------------------------------------------")
    print("\nTest Case 1: Two agents, three resources")
    matrix1 = [
        [81, 19, 1],
        [70, 1, 29]
    ]
    result1 = Egalitarian_division(matrix1)
    print_Div(result1, matrix1)

    print("----------------------------------------------")
    # Test Case 2: More balanced valuations
    print("\n\nTest Case 2: Balanced valuations")
    matrix2 = [
        [50, 50, 50],
        [50, 50, 50],
        [50, 50, 50]
    ]
    result2 = Egalitarian_division(matrix2)
    print_Div(result2, matrix2)

    print("----------------------------------------------")
    # Test Case 3: Highly unbalanced valuations
    print("\n\nTest Case 3: Highly unbalanced valuations")
    matrix3 = [
        [90, 10, 5],
        [5, 90, 10],
        [10, 5, 90]
    ]
    result3 = Egalitarian_division(matrix3)
    print_Div(result3, matrix3)

    print("----------------------------------------------")
    # Test Case 4: More agents and resources
    print("\n\nTest Case 4: Four agents, four resources")
    matrix4 = [
        [40, 30, 20, 10],
        [10, 40, 30, 20],
        [20, 10, 40, 30],
        [30, 20, 10, 40]
    ]
    result4 = Egalitarian_division(matrix4)
    print_Div(result4, matrix4)

    print("----------------------------------------------")
    # Test Case 5: Large value differences
    print("\n\nTest Case 5: Large value differences")
    matrix5 = [
        [100, 1, 1],
        [1, 100, 1],
        [1, 1, 100]
    ]
    result5 = Egalitarian_division(matrix5)
    print_Div(result5, matrix5)

    print("----------------------------------------------")
    # Test Case 6: 2 agents, 2 resources
    print("\n\nTest Case 6: Large value differences")
    matrix6 = [
        [100, 0],
        [0, 100]
    ]
    result6 = Egalitarian_division(matrix6)
    print_Div(result6, matrix6)


if __name__ == "__main__":
    test_egalitarian_division()
