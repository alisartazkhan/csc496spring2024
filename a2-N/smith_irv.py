from collections import defaultdict
from typing import Dict, List, Tuple, Hashable, Optional
import typing

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


def smith_irv(ballots: List[Ballot]) -> Result:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)
    matrix: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2} for c1 in candidates}
    pairwise_matrix: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2} for c1 in candidates}

    return 0, False


scheme: Scheme = smith_irv
name: str = "smith_irv"


def main() -> None:
    shared_main(name, scheme)
    # ballots = [   Ballot(ranking=(1, 0), tally=3),
    # Ballot(ranking=(1, 2), tally=8),
    # Ballot(ranking=(2, 1), tally=2)]
    # result, no_ties = river(ballots)
    # # print(f"Winner: {result}, No ties: {no_ties}")
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