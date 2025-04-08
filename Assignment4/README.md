# 🧮 Huntington–Hill Seat Allocation

This project implements the **Huntington–Hill method** for proportional seat allocation among political parties based on vote counts.  
The method is used, for example, in the United States to assign congressional seats among states.

---

## 🇮🇱 Real Election Data – Israeli Knesset (25th Elections)

The dataset is based on the **25th Knesset elections** in Israel, held on **November 1, 2022**.  
It includes only the parties that passed the electoral threshold.

| Party                        | Valid Votes | Original Seats |
|-----------------------------|-------------|----------------|
| LIKUD                       | 1,115,336   | 32             |
| YESH ATID                   | 847,435     | 24             |
| ZUIONOT AND OZMA            | 516,470     | 14             |
| "MAHNE MMLAHTI              | 432,482     | 12             |
| SHAS                        | 392,964     | 11             |
| UNITED TORAH JUDAISM        | 280,194     | 7              |
| YISRAEL BEITEINU            | 213,687     | 6              |
| UNITED ARAB LIST            | 194,047     | 5              |
| HADASH–TA'AL                | 178,735     | 5              |
| HAAVODA                     | 175,992     | 4              |

📊 Source: [Israel Central Elections Committee](https://votes25.bechirot.gov.il/)

---

## 🧪 Test Case Examples

The code includes built-in test cases to validate the correctness of the algorithm.

### ✅ Test Case 1: 3 Parties, 10 Seats

**Input:**

```python
votes = {"A": 100, "B": 200, "C": 300}
total_seats = 10
```

**Expected Output:**

```python
{"A": 2, "B": 3, "C": 5}
```

---

### ✅ Test Case 2: One party with very few votes

**Input:**

```python
votes = {"A": 100, "B": 200, "C": 1}
total_seats = 10
```

**Expected Output:**

```python
{"A": 3, "B": 6, "C": 1}
```

---

### ✅ Test Case 3: One dominant party

**Input:**

```python
votes = {"A": 100, "B": 200, "C": 10000}
total_seats = 10
```

**Expected Output:**

```python
{"A": 1, "B": 1, "C": 8}
```

---

### ✅ Test Case 4: Two parties with a small vote difference

**Input:**

```python
votes = {"A": 100, "B": 101}
total_seats = 6
```

**Expected Output:**

```python
{"A": 3, "B": 3}
```

---

### ✅ Test Case 5: Party A has twice the votes of Party B

**Input:**

```python
votes = {"A": 100, "B": 50}
total_seats = 6
```

**Expected Output:**

```python
{"A": 4, "B": 2}
```

---

## 🛠️ How to Run

1. Make sure you have Python 3.10+ installed.
2. Run the script using:

```bash
python algo_EX4
```

This will:
- Perform seat allocation using real election data
- Print the difference between original and new seat distribution
- Run 5 test cases and validate correctness using assertions

---

## 📖 Method Summary

The Huntington–Hill method allocates seats using the formula:

```
priority = votes / sqrt(seats * (seats + 1))
```

All parties start with 1 seat to avoid division by zero.  
Remaining seats are distributed one-by-one to the party with the highest priority score.


