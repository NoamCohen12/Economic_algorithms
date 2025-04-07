import math


def huntington_hill_allocation(
        parties: list[str],
        votes: dict[str, int],
        total_seats: int,
        checkY=False,
        Y=0
) -> dict[str, int]:
    """
     Allocate seats using the Huntington–Hill method.
     Each party starts with 1 seat, and remaining seats are assigned
     based on the party with the highest priority.
     """
    # Any party get one seat in the beginning because the quota of any party without seats is infinite.
    # example Licod : 1
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


    Y = 0.000
    step = 0.001
    last_equal_Y = 0.000

    while True:
        new_allocation = huntington_hill_allocation(
            parties, votes, total_seats, checkY=True, Y=Y
        )
        if new_allocation != original_seats:
            print(f"{Y} is the Y that changed the allocation")
            break
        last_equal_Y = Y
        Y += step




