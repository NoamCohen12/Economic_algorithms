# Demonstration of Non-Monotonicity in the Method of Equal Shares (Rule X)

This document addresses **Question 4** from the assignment, which concerns the non-monotonicity of the Equal Shares method as described by Dominik Peters and Piotr Skowron (2020).

## A. Demonstrate non-monotonicity using an example

We consider the following election profile with 4 voters and 4 candidates:

```
Voter 0: {0, 1}
Voter 1: {1}
Voter 2: {2}
Voter 3: {3}
```

We run the Method of Equal Shares for committee sizes `k=2` and `k=3`.

### For k = 2

- Initial budget per voter: 0.5
- Candidate 1 is supported by voters [0, 1] and requires 0.5 per supporter → selected.
- No other candidate can be afforded with the remaining budgets.
- Resulting committee: `{1}`

### For k = 3

- Initial budget per voter: 0.333
- Candidate 1 is supported by voters [0, 1], but needs 0.5 per supporter and they cannot afford it.
- No candidate can be selected.
- Resulting committee: `∅`

**Conclusion**: Candidate 1 is selected for `k=2` but not for `k=3`. This violates monotonicity.

## B. Ensure the example does not depend on tie-breaking

In this profile, at each selection step there is at most one candidate that meets the selection criteria (i.e., enough supporters with sufficient budget).

- In k=2, only Candidate 1 can be selected.
- In k=3, no candidate can be selected.

There is no need to break ties. Hence, the example demonstrates **non-monotonicity without relying on tie-breaking**.

---

