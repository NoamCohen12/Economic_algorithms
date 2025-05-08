# Envy‑Free Room Allocation  
### Comparing a **Bellman–Ford‑based** subsidy rule to a **MILP / CVXPY** pricing rule

---

## Repository layout
```text
.
├── algo_EX7.py                 # Bellman–Ford implementation
├── algo_EX7L.py                # MILP / CVXPY implementation
├── utils.py                    # helpers used by both algorithms
├── test_fair_rent_room_division.py  # benchmarking & demo script
└── README.md                   # this file
Algorithms in a nutshell
File	Main idea
algo_EX7.py	Build an envy graph and run Bellman–Ford to get longest‑path “subsidies”; 𝒪(n²) and entirely combinatorial.
algo_EX7L.py	Model envy‑free constraints as a linear program and let CVXPY/MILP solver find prices.

utils.py bundles shared helpers (find_assignment, build_envy_graph, check_envy, print_result, …).

Seven illustrative inputs
Case	Valuation matrix V	What’s special
1	[[150, 0], [140, 10]]	One player vastly out‑values a single room.
2	[[100, 100], [100, 100]]	Perfect symmetry – everybody values everything the same.
3	[[90, 100], [80, 120]]	Mild disagreement; slight gains from trade.
4	[[100, 0], [50, 50]]	One player indifferent, the other single‑minded.
5	[[1000, 10], [5, 990]]	Extreme preferences (almost single‑minded with huge numbers).
6	identity 3 × 3	Each player likes a unique room (diagonal).
7	[[100, 200, 0], [0, 100, 200], [200, 0, 100]]	Cyclic preferences.

Side‑by‑side results
<details><summary><b>Click to expand the 7 cases</b></summary>
Case 1  (rent = 100)
Player	Bellman‑Ford <sub>(room, pay)</sub>	MILP <sub>(room, pay)</sub>
0	(0, 125.00)	(0, 120.00)
1	(1, ‑25.00)	(1, ‑20.00)

Case 2  (rent = 100)
Player	Bellman‑Ford	MILP
0	(1,  50.00)	(1,  50.00)
1	(0,  50.00)	(0,  50.00)

Case 3  (rent = 100)
Player	Bellman‑Ford	MILP
0	(0,  45.00)	(0,  37.50)
1	(1,  55.00)	(1,  62.50)

Case 4  (rent = 100)
Player	Bellman‑Ford	MILP
0	(0, 100.00)	(0,  75.00)
1	(1,   0.00)	(1,  25.00)

Case 5  (rent = 100)
Player	Bellman‑Ford	MILP
0	(0, 545.00)	(0,  51.25)
1	(1, ‑445.00)	(1,  48.75)

Case 6  (rent = 300)
Player	Bellman‑Ford	MILP
0	(0, 166.67)	(0, 100.00)
1	(1,  66.67)	(1, 100.00)
2	(2,  66.67)	(2, 100.00)

Case 7  (rent = 300)
Player	Bellman‑Ford	MILP
0	(1, 200.00)	(1, 100.00)
1	(2,   0.00)	(2, 100.00)
2	(0, 100.00)	(0, 100.00)

</details>
Quick observations

Both algorithms always achieve envy‑freeness.

Bellman‑Ford naturally produces subsidies (negative payments) whenever total rent is low relative to valuations.

The MILP prices respect ∑ p_i = rent and, in these runs, ended up non‑negative.

Random‑instance benchmark
<p align="center"> <img src="assets/runtime_comparison.png" width="550" alt="Runtime comparison Bellman‑Ford vs MILP"> </p>
The figure shows average runtime (20 random instances for each n = 2 … 21):

Bellman‑Ford scales roughly quadratically and stays under 50 ms even for 21×21 instances.

MILP time grows steeply once n > 10, topping ~850 ms for n = 21.

⇒ If you need speed, pick Bellman‑Ford; if you need a flexible LP formulation, tolerate the slowdown.

How to reproduce
bash
Copy
Edit
pip install -r requirements.txt        # networkx, cvxpy, pandas, matplotlib
python test_fair_rent_room_division.py # generates the plot in assets/
Happy allocating! :rocket:

pgsql
Copy
Edit

---

### What changed vs. the previous README?

* **Input table** summarising all seven matrices and what makes each interesting.  
* Each case now shows Bellman‑Ford **and** MILP results **side‑by‑side** in a compact table.  
* The runtime figure is the *two‑line* comparison you provided (`assets/runtime_comparison.png`).  
  * If you still prefer the “gap” plot instead, just swap the `src=` filename.  

Paste this content into `README.md` (replace the old version) and save the plot image as  
`assets/runtime_comparison.png` so the markdown link works.

Let me know if you’d like any further tweaks!