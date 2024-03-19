from collections import Counter
from typing import Hashable, Set

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


# def redistribute_ballots(ballots: list[Ballot], eliminated_candidates: Set[Hashable]):
#     for c in eliminated_candidates:
#         for ballot in ballots:
#             ballot.ranking = tuple(list(ballot.ranking).remove(c))
    
def borda(ballots: list[Ballot], eliminated_candidates: Set[Hashable]) -> list[Hashable]:
    size: int = 0
    for ballot in ballots:
        s = 0
        for c in ballot.ranking:
            if c not in eliminated_candidates:
                s +=1
        if s > size:
            size = s
    
    points: list[int] = [c for c in range(size - 1, -1, -1)]
    scores: Counter[Hashable] = Counter()
    for ballot in ballots:
        for i, candidate in enumerate(ballot.ranking):
            if candidate not in eliminated_candidates:
                scores[candidate] += points[i] * ballot.tally
    min_score: int = min(scores.values())
    losers: list[Hashable] = [candidate for candidate, score in scores.items() if score == min_score]
    return losers


def baldwin(ballots: list[Ballot]) -> Result:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)
    eliminated_candidates: Set[Hashable] = set()
    winners = candidates ^ eliminated_candidates

    while len(winners) != 1:
        losers: list[Hashable] = borda(ballots, eliminated_candidates)
        if len(losers) != 1:
            return 0, False
        eliminated_candidates = eliminated_candidates.union(set(losers))
        # redistribute_ballots(ballots, eliminated_candidates)
        winners = candidates ^ eliminated_candidates

    

    return winners[0], True

scheme: Scheme = baldwin
name: str = "baldwin"


def main() -> None:
    shared_main(name, scheme)
    ballots = [  Ballot(ranking=(0, 2), tally=4),
    Ballot(ranking=(2, 1), tally=9)]
    result, no_ties = baldwin(ballots)
    print(f"Winner: {result}, No ties: {no_ties}")

if __name__ == "__main__":
    main()
