
import importlib
import random
import time

import matplotlib

matplotlib.use("TkAgg")  # change to "Agg" or "QtAgg" if preferred

import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------------------
#  user modules  -------------------------------------------------------------
# ---------------------------------------------------------------------------
mod_bf = importlib.import_module("algo_EX7")  # Bellman‑Ford based version
mod_lp = importlib.import_module("algo_EX7L")  # MILP / cvxpy based version


# ---------------------------------------------------------------------------
#  helpers  ------------------------------------------------------------------
# ---------------------------------------------------------------------------

def random_instance(n: int, vmin: int = 0, vmax: int = 200):
    """create a random valuation matrix(n×n) and total rent = mean value"""
    vals = [[random.randint(vmin, vmax) for _ in range(n)] for _ in range(n)]
    rent = sum(sum(vals, [])) / n  # average entry
    return vals, rent


def run_bf(vals, rent):
    t0 = time.perf_counter()
    try:
        mod_bf.envy_free_room_allocation(vals, rent)
    except TypeError:
        # implementation prints but does not return → still measure time
        pass
    return (time.perf_counter() - t0) * 1000  # ms


def run_lp(vals, rent):
    t0 = time.perf_counter()
    mod_lp.envy_free_room_allocation_L(vals, rent)
    return (time.perf_counter() - t0) * 1000  # ms


# ---------------------------------------------------------------------------
#  experiment  ---------------------------------------------------------------
# ---------------------------------------------------------------------------
rows = []
for n in range(2, 22):  # sizes 2 .. 21 (inclusive)
    vals, rent = random_instance(n)
    rows.append({"n": n, "algo": "Bellman‑Ford", "time_ms": run_bf(vals, rent)})
    rows.append({"n": n, "algo": "MILP", "time_ms": run_lp(vals, rent)})

df = pd.DataFrame(rows)

# pivot for difference plot
pivot = df.pivot(index="n", columns="algo", values="time_ms")
pivot["gap_ms"] = pivot["Bellman‑Ford"] - pivot["MILP"]  # >0  ⇒  BF slower

# ---------------------------------------------------------------------------
#  figure –runtime curves  -------------------------------------------------
# ---------------------------------------------------------------------------
plt.figure()
for algo in df["algo"].unique():
    subset = df[df["algo"] == algo]
    plt.plot(subset["n"], subset["time_ms"], marker="o", label=algo)
plt.xlabel("Number of rooms / players (n)")
plt.ylabel("Runtime (ms)")
plt.title("Runtime comparison: Bellman‑Ford vs. MILP")
plt.grid(True)
plt.legend()

plt.show()
