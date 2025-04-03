
# 🧮 Competitive Equilibrium Model (Logarithmic Utilities)

This project implements a **logarithmic utility-based competitive equilibrium algorithm** in Python using the `cvxpy` optimization library.

The goal is to allocate limited resources to multiple players, each with their own preferences and budgets, in a way that maximizes the **sum of weighted log utilities**. The result reflects both **efficiency** and **fairness**.

---

## ▶️ How to Run

Make sure you have `cvxpy` installed:

```bash
pip install cvxpy
```

Then run the script:

```bash
python algo_EX3.py
```

---

## 📊 Output Summary

Below are the results for five different economic scenarios, including inputs, allocations, equilibrium prices, and player utilities.

---

### ✅ Example 1 - Original

**Inputs:**
```python
values = [
    [8, 4, 2],
    [2, 6, 5],
    [1, 3, 7]
]
budgets = [60, 40, 30]
supply  = [1, 1, 1]
```

**Allocation Matrix:**
```
Player 1 :  1.00  0.00  0.00
Player 2 :  0.00  1.00  0.06
Player 3 :  0.00  0.00  0.94
```

**Prices:** 59.9996, 38.1816, 31.8180  
**Utilities:** 8.0000, 6.2857, 6.6000

---

### ✅ Example 2 - Distinct Preferences

**Inputs:**
```python
values = [
    [10, 2, 1],
    [1, 9, 1],
    [1, 1, 10]
]
budgets = [60, 40, 30]
supply  = [1, 1, 1]
```

**Allocation Matrix:**
```
Player 1 :  1.00  0.00  0.00
Player 2 :  0.00  1.00  0.00
Player 3 :  0.00  0.00  1.00
```

**Prices:** 60.0000, 39.9999, 30.0001  
**Utilities:** 10.0000, 9.0000, 10.0000

---

### ✅ Example 3 - Overlapping Preferences

**Inputs:**
```python
values = [
    [5, 3, 2],
    [4, 4, 2],
    [3, 2, 5]
]
budgets = [100, 100, 100]
supply  = [1, 1, 1]
```

**Allocation Matrix:**
```
Player 1 :  1.00  0.00  0.00
Player 2 :  0.00  1.00  0.00
Player 3 :  0.00  0.00  1.00
```

**Prices:** 100.0000, 99.9996, 99.9997  
**Utilities:** 5.0000, 4.0000, 5.0000

---

### ✅ Example 4 - Wealthy Player

**Inputs:**
```python
values = [
    [6, 6, 6],
    [1, 5, 3],
    [2, 2, 8]
]
budgets = [200, 50, 50]
supply  = [1, 1, 1]
```

**Allocation Matrix:**
```
Player 1 :  1.00  0.50  0.50
Player 2 :  0.00  0.50  0.00
Player 3 :  0.00  0.00  0.50
```

**Prices:** 99.9998, 99.9996, 100.0000  
**Utilities:** 12.0000, 2.5000, 4.0000

---

### ✅ Example 5 - Identical Preferences

**Inputs:**
```python
values = [
    [5, 5, 5],
    [5, 5, 5],
    [5, 5, 5]
]
budgets = [30, 40, 30]
supply  = [1, 1, 1]
```

**Allocation Matrix:**
```
Player 1 :  0.30  0.30  0.30
Player 2 :  0.40  0.40  0.40
Player 3 :  0.30  0.30  0.30
```

**Prices:** 33.3334, 33.3334, 33.3334  
**Utilities:** 4.5000, 5.9999, 4.5000

---

## 🧠 Notes

- The algorithm solves a convex optimization problem using `cvxpy`.
- Prices are derived from the dual variables of the supply constraints.
- Utilities are calculated as the sum of allocated value per player.
- Each scenario tests different market dynamics: competition, equality, dominance, and fairness.

---
