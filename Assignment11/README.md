# Budget Decomposition Checker

This project solves a budget decomposition problem, based on a fair allocation model.

## 🧠 Problem Definition

Given:
- A list of `m` topics (columns)
- A list of `n` citizens (rows)
- A required budget for each topic: `budget[j]`
- A list of preferences `preferences[i]` – each citizen only donates to topics they support

We want to determine whether the total budget `C = sum(budget)` can be distributed so that:

1. Each citizen donates exactly `C / n`
2. Each topic receives exactly `budget[j]`
3. Citizens donate **only** to topics they support

This is called a **decomposable budget**.

---

## 📥 Input

- `budget: list[float]` — required budget per topic
- `preferences: list[set[int]]` — for each citizen, the set of topic indices they support

---

## 📤 Output

- If a legal allocation exists: prints a table `[citizens × topics]` showing donation amounts
- Otherwise: raises an error indicating the budget is **not decomposable**

---

## 📦 Example Usage

```python
budget = [400, 50, 50, 0]
preferences = [{0, 1}, {0, 2}, {0, 3}, {1, 2}, {0}]
matrix = find_decomposition(budget, preferences)
print_allocation_table(matrix)
```

📋 Output:
```
✅ Found a legal allocation:

📊 Allocation Table:
           Topic 0  Topic 1  Topic 2  Topic 3
Citizen 0   100.00     0.00     0.00     0.00
Citizen 1   100.00     0.00     0.00     0.00
Citizen 2   100.00     0.00     0.00     0.00
Citizen 3     0.00    50.00    50.00     0.00
Citizen 4   100.00     0.00     0.00     0.00
```

---

## ❌ Example of Infeasibility

```python
budget = [250, 250, 100]
preferences = [{0}, {1}, {2}]
matrix = find_decomposition(budget, preferences)
```

Output:
```
❌ ValueError: No legal allocation found. Problem status: infeasible
```

---

## 🧪 Requirements

- Python 3.9+
- `cvxpy`
- `numpy`
- `pandas`

Install dependencies:
```bash
pip install cvxpy numpy pandas
```

---

## 🛠 Files

- `algo-EX11.py` — main script
- `README.md` — this file

---

## 🧑‍💻 Author

Developed as part of an academic assignment in economic algorithms.
