from typing import List
import numpy as np


def generate_linear_fixed_votes(
    total_budget: float,
    num_citizens: int,
    num_topics: int,
    t: float
) -> List[List[float]]:
    """
    Generates n−1 fixed votes using linear functions fi(t) = C * min(1, i * t).
    Each fixed vote is a uniform vector across all topics.
    """
    fixed_votes = []
    for i in range(1, num_citizens):
        row = [total_budget * min(1.0, i * t) for _ in range(num_topics)]
        fixed_votes.append(row)
    return fixed_votes


def allocation_for_t(
    t: float,
    total_budget: float,
    citizen_votes: List[List[float]]
) -> List[float]:
    """
    Combines citizen votes with fixed votes and computes the median
    allocation per topic for a given value of t.
    """
    num_citizens = len(citizen_votes)
    num_topics = len(citizen_votes[0])
    fixed_votes = generate_linear_fixed_votes(total_budget, num_citizens, num_topics, t)
    all_votes = citizen_votes + fixed_votes

    medians = []

    for topic_index in range(num_topics):
        topic_scores = []

        for vote in all_votes:
            topic_scores.append(vote[topic_index])  # Extract score for this topic

        topic_median = np.median(topic_scores)  # Compute the median score
        medians.append(topic_median)

    return medians


def sum_of_allocation(
    t: float,
    total_budget: float,
    citizen_votes: List[List[float]]
) -> float:
    """
    Returns the total allocated budget across all topics for a given t.
    """
    return sum(allocation_for_t(t, total_budget, citizen_votes))


def compute_budget(
    total_budget: float,
    citizen_votes: List[List[float]]
) -> List[float]:
    """
    Uses binary search over t ∈ [0,1] to find the allocation vector
    whose entries sum up to the total budget.
    """
    low, high = 0.0, 1.0
    best_t = 0.0
    for _ in range(100):  # sufficient for precision of 1e-6
        mid = (low + high) / 2
        best_t = mid
        current_total = sum_of_allocation(mid, total_budget, citizen_votes)
        if current_total > total_budget:
            high = mid
        else:
            low = mid

    print(f"Best t found: {best_t}, Total allocation: {sum_of_allocation(best_t, total_budget, citizen_votes)}")
    return allocation_for_t(best_t, total_budget, citizen_votes)


if __name__ == "__main__":
    votes1 = [
        [100, 0, 0],    # Citizen 1 supports topic 0
        [0, 0, 100]     # Citizen 2 supports topic 2
    ]
    total_budget1 = 100
    result1 = compute_budget(total_budget1, votes1)
    print(result1)
    # Expected output: [50.0, 0.0, 50.0]

    total_budget2 = 30
    votes2 = [
        [6, 6, 6, 6, 0, 0, 6, 0, 0],  # Citizen A
        [0, 0, 6, 6, 6, 6, 0, 6, 0],  # Citizen B
        [6, 6, 0, 0, 6, 6, 0, 0, 6]   # Citizen C
    ]
    result2 = compute_budget(total_budget2, votes2)
    print(result2)