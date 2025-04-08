import math


def huntington_hill_allocation(
        parties: list[str],
        votes: dict[str, int],
        total_seats: int,
        checkY=False,
        Y=0,
        test=False
) -> dict[str, int]:
    """
     Allocate seats using the Huntington–Hill method.
     Each party starts with 1 seat, and remaining seats are assigned
     based on the party with the highest priority.
     """
    # Any party get one seat in the beginning because the quota of any party without seats is infinite.
    # example LIKUD : 1
    seats = {party: 1 for party in parties}
    if checkY:
        print(f"Using {Y} ")
    while sum(seats.values()) < total_seats:
        # Calculate the priority for each party
        # based the formula - f(s) = votes / sqrt(s * (s + 1))
        if checkY:
            priorities = {
                party: votes[party] / (seats[party] + Y)
                for party in parties
            }
        else:
            priorities = {
                party: votes[party] / math.sqrt(seats[party] * (seats[party] + 1))
                for party in parties
            }
        # find the party:str with the maximum priority
        max_party = max(priorities, key=priorities.get)
        # give to the party with max priorities one more seat
        seats[max_party] += 1
        if test:
            print(f"\n--- Round {sum(seats.values()) - len(parties) + 1} ---")
            print(f"Current seat distribution: {seats}")
            print("Priorities:")
            for p in priorities:
                print(f"{p}: {priorities[p]:.2f}")
            print(f"=> {max_party} gets a seat (now has {seats[max_party]})")
    return seats


# https://votes25.bechirot.gov.il/
# The data is from the Knesset25 elections in Israel.
# Parties that passed the electoral threshold
data = [
    ["LIKUD", 1115336, 32],
    ["YESH ATID", 847435, 24],
    ["ZUIONOT AND OZMA", 516470, 14],
    ["MAHNE MMLAHTI", 432482, 12],
    ["SHAS", 392964, 11],
    ["UNITED TORAH JUDAISM", 280194, 7],
    ["YISRAEL BEITEINU", 213687, 6],
    ["UNITED ARAB LIST", 194047, 5],
    ["HADASH–TA'AL", 178735, 5],
    ["HAAVODA", 175992, 4],
]


def print_comparison(
        allocation: dict[str, int],
        original_seats: dict[str, int]) -> None:
    """
    Print the comparison between the original and new allocation of seats.
    """
    print(f"{'Party':<25} {'Original':<10} {'New':<10} {'Diff':<10}")
    print("-" * 55)
    for party in allocation:
        original = original_seats[party]
        new = allocation[party]
        diff = new - original
        print(f"{party:<25} {original:<10} {new:<10} {diff:<+10}")


def test_huntington_hill_allocation() -> None:
    """
    Test the huntington_hill_allocation function.
    """
    print("\n--- Testing Huntington-Hill Allocation ---")
    print("Test case 1: Basic test with 3 parties and 10 seats")
    parties = ["A", "B", "C"]
    votes1 = {"A": 100, "B": 200, "C": 300}
    total_seats = 10
    expected_allocation1 = {"A": 2, "B": 3, "C": 5}
    allocation1 = huntington_hill_allocation(parties, votes1, total_seats)
    assert allocation1 == expected_allocation1, f"Expected {expected_allocation1}, but got {allocation1}"

    print("Test case 2: party with little votes")
    votes2 = {"A": 100, "B": 200, "C": 1}
    expected_allocation2 = {"A": 3, "B": 6, "C": 1}
    allocation2 = huntington_hill_allocation(parties, votes2, total_seats)
    assert allocation2 == expected_allocation2, f"Expected {expected_allocation2}, but got {allocation2}"

    print("Test case 3: party with many votes")
    votes3 = {"A": 100, "B": 200, "C": 10000}
    expected_allocation3 = {"A": 1, "B": 1, "C": 8}
    allocation3 = huntington_hill_allocation(parties, votes3, total_seats)
    assert allocation3 == expected_allocation3, f"Expected {expected_allocation3}, but got {allocation3}"

    print("Test case 4: party with small difference in votes")
    parties4 = ["A", "B"]
    votes4 = {"A": 100, "B": 101}
    expected_allocation4 = {"A": 3, "B": 3}
    total_seats4 = 6
    allocation4 = huntington_hill_allocation(parties4, votes4, total_seats4)
    assert allocation4 == expected_allocation4, f"Expected {expected_allocation4}, but got {allocation4}"

    print("Test case 5: 2 parties, party A has twice the votes of party B")
    parties5 = ["A", "B"]
    votes5 = {"A": 100, "B": 50}
    expected_allocation5 = {"A": 4, "B": 2}
    total_seats5 = 6
    allocation5 = huntington_hill_allocation(parties5, votes5, total_seats5)
    assert allocation5 == expected_allocation5, f"Expected {expected_allocation5}, but got {allocation5}"


if __name__ == "__main__":
    parties = [row[0] for row in data]
    votes = {row[0]: row[1] for row in data}
    total_seats = 120
    original_seats = {row[0]: row[2] for row in data}

    allocation = huntington_hill_allocation(parties, votes, total_seats, checkY=False)
    print_comparison(allocation, original_seats)

    # for party in allocation:
    #     print(f"{party} get {original_seats[party]} seats in the original"
    #           f" allocation and {allocation[party]} seats in the new allocation")
    test_huntington_hill_allocation()
