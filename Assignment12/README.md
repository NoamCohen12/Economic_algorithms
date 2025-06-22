# Budget Allocation Using Median and Binary Search

This Python module implements a mechanism for computing a fair allocation of a fixed budget across multiple topics, based on citizen votes and linear fixed votes.

## Description

The core idea is to compute the median allocation for each topic, combining citizen votes and a set of fixed, linearly scaled votes parameterized by `t`. The goal is to find a value of `t` such that the total allocated budget is equal to the desired total budget. This is achieved via binary search.

## Input

- `total_budget` (float): The total amount of budget to be distributed among topics.
- `citizen_votes` (List[List[float]]): A list where each sublist represents a citizen's support vector for the topics.

Each inner list must be of equal length (number of topics).

## Output

- A list of floats representing the final budget allocation per topic. The sum of the list will be approximately equal to `total_budget`.

## Main Functions

- `generate_linear_fixed_votes(...)`: Generates n−1 fixed votes using `fi(t) = C * min(1, i * t)`.
- `allocation_for_t(...)`: Computes the median allocation vector for a given `t`.
- `sum_of_allocation(...)`: Computes the sum of allocations for a given `t`.
- `compute_budget(...)`: Uses binary search to find the appropriate `t` that yields a valid allocation.

## Requirements

- Python 3.7+
- NumPy

## Running the Code

```bash
python your_script_name.py
```

Replace `your_script_name.py` with the actual filename.

## Example Inputs and Outputs

### Example 1

**Input:**
```python
votes1 = [
    [100, 0, 0],    # Citizen 1 supports topic 0
    [0, 0, 100]     # Citizen 2 supports topic 2
]
total_budget1 = 100
result1 = compute_budget(total_budget1, votes1)
print([int(x) for x in result1])
```

**Output:**
```text
Best t found: 0.5, Total allocation: 100.0
[50, 0, 50]
```

---

### Example 2

**Input:**
```python
votes2 = [
    [6, 6, 6, 6, 0, 0, 6, 0, 0],  # Citizen A
    [0, 0, 6, 6, 6, 6, 0, 6, 0],  # Citizen B
    [6, 6, 0, 0, 6, 6, 0, 0, 6]   # Citizen C
]
total_budget2 = 30
result2 = compute_budget(total_budget2, votes2)
print([result2])
```

**Output:**
```text
Best t found: 0.06666666666666668, Total allocation: 30.000000000000004
[4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 2.0, 2.0]
```