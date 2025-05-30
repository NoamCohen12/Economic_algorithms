from abcvoting.preferences import Profile


def Equal_Shares(profile, k):
    num_voters = len(profile)
    budget = [1.0 / k] * num_voters
    committee = set()
    candidates = set(range(profile.num_cand))
    print("\n=== Election Profile ===")
    print(profile)
    print(f"\n--- Running Rule X for k={k}, n={num_voters} ---")
    print(f"• Initial budget per voter = k/n = {round(1.0 / k, 3)}")
    print(f"• Total voters: {num_voters}, candidates: {profile.num_cand}")
    print(f"• Budgets at start: {[round(b, 3) for b in budget]}")

    while len(committee) < k:
        viable = []

        for c in sorted(candidates - committee):
            supporters = [i for i, ballot in enumerate(profile) if c in ballot.approved]
            if not supporters:
                continue

            cost_per_voter = 1.0 / len(supporters)
            total_budget = sum(budget[i] for i in supporters)

            print(f"\n→ Checking candidate {c}: supported by voters {supporters}")
            print(
                f"  • Required {round(cost_per_voter, 3)} per supporter (total {round(len(supporters) * cost_per_voter, 3)})")
            print(f"  • Total budget of supporters: {round(total_budget, 3)}")

            if all(budget[i] >= cost_per_voter for i in supporters):
                print("  ✅ This candidate can be selected.")
                viable.append((cost_per_voter, c, supporters))
            else:
                print("  ❌ Cannot select this candidate (insufficient budget).")

        if not viable:
            print("\n❌ No additional candidate can be funded. Stopping.")
            break

        cost, chosen_cand, supporters = min(viable)
        print(f"\n✅ Candidate {chosen_cand} selected (supported by {supporters}, cost per supporter: {round(cost, 3)})")
        committee.add(chosen_cand)

        for i in supporters:
            budget[i] -= cost

        print(f"Remaining budget after this round: {[round(b, 3) for b in budget]}")

    return committee


def IsMonotonic(result_k2: set, result_k3: set):
    """
    Check if the result for k=2 is a subset of the result for k=3.
    """
    removed = set(result_k2) - set(result_k3)
    if removed:
        print(f"\n❗ Non-monotonicity: candidate(s) {removed} were selected for k=2 but not for k=3")
    else:
        print("\n✅ Monotonic result (all members of committee of size 2 were also selected for size 3)")


if __name__ == "__main__":
    profile = Profile(num_cand=4)
    profile.add_voter({0, 1})
    profile.add_voter({1})
    profile.add_voter({2})
    profile.add_voter({3})

    print("\n=== Committee of size 2 ===")
    committee2 = Equal_Shares(profile, 2)
    print(f"\nCommittee of size 2: {committee2}")

    print("\n=== Committee of size 3 ===")
    committee3 = Equal_Shares(profile, 3)
    if len(committee3) == 0:
        print("No committee could be formed for k=3.")
    else:
        print(f"\nCommittee of size 3: {committee3}")

    IsMonotonic(committee2, committee3)
