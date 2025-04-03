# 🧮 Competitive Equilibrium Model (Logarithmic Utilities)

This project implements a **logarithmic utility-based competitive equilibrium model** using Python and `cvxpy`.

The model allocates limited resources among players, considering their **preferences** and **budgets**, in a way that maximizes the **sum of weighted log utilities**. This reflects a fair and efficient outcome in resource allocation.

---

## ▶️ How to Run

1. Install dependencies:
```bash
pip install numpy cvxpy
```

2. Run the script:
```bash
python algo_EX3.py
```

---

## 📊 Output Summary

The script computes equilibria for five economic scenarios and displays allocations, prices, and player utilities.

---

### ✅ Example 1 – Original

**Inputs:**
```python
values = [
    [8, 4, 2],
    [2, 6, 5]
]
budgets = [60, 40]
```

**Allocation Matrix:**
```
Player 1 :  1.00  0.30  0.00  
Player 2 :  0.00  0.70  1.00
```

**Prices:** 52.1741, 26.0869, 21.7389  
**Utilities:** 9.2000, 9.2000

📌 *Despite different valuations, the market clears with equal utility.*

---

### ✅ Example 2 – Zero Valuations

**Inputs:**
```python
values = [
    [10, 0, 5],
    [0, 8, 6]
]
budgets = [50, 50]
```

**Allocation Matrix:**
```
Player 1 :  1.00  0.00  0.17  
Player 2 :  0.00  1.00  0.83
```

**Prices:** 46.1538, 30.7692, 23.0769  
**Utilities:** 10.8333, 13.0000

📌 *Each player ignores resources they don't value — efficient specialization.*

---

### ✅ Example 3 – Low Budgets

**Inputs:**
```python
values = [
    [4, 3, 2],
    [5, 1, 1]
]
budgets = [1, 1]
```

**Allocation Matrix:**
```
Player 1 :  0.00  1.00  1.00  
Player 2 :  1.00  0.00  0.00
```

**Prices:** 1.0000, 0.6000, 0.4000  
**Utilities:** 5.0000, 5.0001

📌 *Even with small budgets, players receive reasonable allocations.*

---

### ✅ Example 4 – High Budgets, Same Values

**Inputs:**
```python
values = [
    [5, 3, 2],
    [5, 3, 2],
    [5, 3, 2]
]
budgets = [10, 10, 80]
```

**Allocation Matrix:**
```
Player 1 :  0.14  0.05  0.06  
Player 2 :  0.14  0.05  0.06  
Player 3 :  0.71  0.90  0.87
```

**Prices:** 50.0001, 30.0001, 20.0001  
**Utilities:** 1.0000, 1.0000, 8.0000

📌 *Player 3 dominates the market due to their large budget, despite identical preferences.*

---

### ✅ Example 5 – Single Resource Preference

**Inputs:**
```python
values = [
    [0, 0, 10],
    [5, 5, 5]
]
budgets = [40, 60]
```

**Allocation Matrix:**
```
Player 1 :  0.00  0.00  1.00  
Player 2 :  1.00  1.00  0.00
```

**Prices:** 30.0001, 30.0001, 40.0003  
**Utilities:** 10.0000, 10.0000

📌 *Player 1 fully consumes their only valued resource. Player 2 uses the rest.*

---

## 🧠 Notes

- The model solves a **convex optimization problem** using `cvxpy`.
- **Resource prices** are derived from the **dual values** of supply constraints.
- The model demonstrates fairness, efficiency, and the effects of **budgets** and **preferences** in resource allocation.
