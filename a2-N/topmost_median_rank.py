from collections import defaultdict
from typing import Dict, List, Tuple, Hashable, Optional
import typing

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


def topmost_median_rank(ballots: List[Ballot]) -> Result:
    # Sort the ballots based on the first element of the ranking tuple
    sorted_ballots: List[Ballot] = sorted(ballots, key=lambda x: x.ranking[0])

    # Calculate the median index
    median_index: int = len(sorted_ballots) // 2

    # Get the winner from the median index
    winner:Hashable = sorted_ballots[median_index].ranking[0]

    # Check for ties by comparing the medians of both halves
    no_ties: bool = sorted_ballots[median_index - 1].ranking[0] != winner

    return winner, no_ties


scheme: Scheme = topmost_median_rank
name: str = "topmost_median_rank"


def main() -> None:
    # shared_main(name, scheme)
    ballots = [   Ballot(ranking=(1, 0), tally=3),
    Ballot(ranking=(1, 2), tally=8),
    Ballot(ranking=(2, 1), tally=2)]
    result, no_ties = topmost_median_rank(ballots)
    print(f"Winner: {result}, No ties: {no_ties}")
    # one = Node(1)
    # two = Node(2)
    # three = Node(3)

    # one.add_child(two)
    # two.add_child(three)
    # three.add_child(one)
    # # print(one)
    # # print(two)
    # # print(three)


if __name__ == "__main__":
    main()