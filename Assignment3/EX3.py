import numpy as np
import cvxpy as cp


def print_result(values, supply=None, budgets=None, example_name=""):
    """
    Run a competitive equilibrium example and print the results.
    """
    alloc, prices = compute_equilibrium(values, supply, budgets)
    utilities = np.sum(alloc * values, axis=1)

    num_players, num_resources = values.shape

    print(f"\n=== Competitive Equilibrium {example_name} ===\n")

    # Allocation Table
    print("Allocation Matrix (Players × Resources):")
    header = "          " + "  ".join([f"R{j + 1:>2}" for j in range(num_resources)])
    print(header)
    for i in range(num_players):
        row_values = "  ".join([f"{alloc[i, j]:>5.2f}" for j in range(num_resources)])
        print(f"Player {i + 1:<2}:  {row_values}")

    print("\nResource Prices:")
    for j in range(num_resources):
        print(f"Resource {j + 1:<2}:  Price = {prices[j]:.4f}")

    print("\nUtility Per Player:")
    for i in range(num_players):
        print(f"Player {i + 1:<2}:  Utility = {utilities[i]:.4f}")

    print("\n" + "=" * 40 + "\n")


# If supply and budgets are not provided:
# - supply will default to a vector of 1s (one per resource)
# - budgets will default to a vector of 1s (one per player)
def set_defaults(supply, budgets, num_players, num_resources):
    if supply is None:
        supply = np.ones(num_resources)
    if budgets is None:
        budgets = np.ones(num_players)
    return supply, budgets


def compute_equilibrium(values, supply=None, budgets=None):
    """
    Compute competitive equilibrium using a budget-weighted logarithmic utility function.

    Args:
        values: Player x Resource value matrix (each row = player's valuation for resources)
        supply: Vector of resource supply (default is 1 unit each)
        budgets: Vector of player budgets (default is equal budgets)

    Returns:
        X: Allocation matrix (players x resources)
        p: Resource prices
    """
    num_players, num_resources = values.shape

    # Defaults
    supply, budgets = set_defaults(supply, budgets, num_players, num_resources)

    # Allocation variables (x[i][j] is allocation of resource j to player i)
    allocation = cp.Variable((num_players, num_resources), nonneg=True)

    # Utility per player = dot product of their values and allocations
    utilities = cp.sum(cp.multiply(values, allocation), axis=1)

    # Weighted log utility objective
    log_util = cp.multiply(budgets, cp.log(utilities))
    objective = cp.Maximize(cp.sum(log_util))

    # Resource constraints: total allocated per resource <= supply
    constraints = [cp.sum(allocation, axis=0) <= supply]

    # Solve the optimization problem
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.SCS)

    X = allocation.value
    p = constraints[0].dual_value

    return X, p


# Main examples
if __name__ == "__main__":
    supply = np.array([1, 1, 1], dtype=float)

    # Example 1: Original from presentation
    values1 = np.array([
        [8, 4, 2],
        [2, 6, 5]
    ], dtype=float)
    budgets1 = np.array([60, 40], dtype=float)
    print_result(values1, supply, budgets1, "Example 1 - Original")

    # Example 2: Each player wants a different resource
    values2 = np.array([
        [10, 2, 1],
        [1, 9, 1]
    ], dtype=float)
    print_result(values2, supply, budgets1, "Example 2 - Distinct Preferences")

    # Example 3: Similar preferences, same budgets
    values3 = np.array([
        [5, 3, 2],
        [4, 4, 2]
    ], dtype=float)
    budgets3 = np.array([100, 100], dtype=float)
    print_result(values3, supply, budgets3, "Example 3 - Overlapping Preferences")

    # Example 4: One rich player
    values4 = np.array([
        [6, 6, 6],
        [1, 5, 3],
        [2, 2, 8]
    ], dtype=float)
    budgets4 = np.array([200, 50, 50], dtype=float)
    print_result(values4, supply, budgets4, "Example 4 - Wealthy Player")

    # Example 5: Identical preferences
    values5 = np.array([
        [5, 5, 5],
        [5, 5, 5],
        [5, 5, 5]
    ], dtype=float)
    budgets5 = np.array([30, 40, 30], dtype=float)
    print_result(values5, supply, budgets5, "Example 5 - Identical Preferences")
