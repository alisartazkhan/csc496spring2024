from collections import Counter, defaultdict
from itertools import permutations
from typing import Dict, Hashable, List
from itertools import product

from common.types import Ballot, Result, Scheme

def pairwise_rankings(ballots: List[Ballot]) -> Dict[Hashable, Dict[Hashable, int]]:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)
    pairwise: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2} for c1 in candidates}
    for ballot in ballots:
        for i, candidate1 in enumerate(ballot.ranking):
            for j in range(i + 1, len(ballot.ranking)):
                candidate2 = ballot.ranking[j]
                pairwise[candidate1][candidate2] += ballot.tally

    for ballot in ballots:
        cs = set(ballot.ranking)
        missing_candidates = candidates - cs
        permutations_between_sets = list(product(cs, missing_candidates))
        for w, l in permutations_between_sets:
            pairwise[w][l] += ballot.tally
    print("PAIRWISE: ", pairwise)
    return pairwise

def kemeny_young(ballots: List[Ballot]) -> Result:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)
    pairwise: Dict[Hashable, Dict[Hashable, int]] = pairwise_rankings(ballots)
    m = 0
    scores = {}
    for c, d in pairwise.items():
        # print(d)
        s = sum(d.values())
        scores[c] = s

    m = max(scores.values())
    winners = [candidate for candidate in scores if scores[candidate] == m]

    # perm = min(permutations(candidates), key=lambda p: sum(pairwise.get((p[i], p[j]), 0) for i in range(len(candidates)) for j in range(i+1, len(candidates))))
    # winners = [candidate for candidate in perm if perm.index(candidate) == 0]
    return winners[0], len(winners) == 1

def main() -> None:
    # shared_main(name, scheme)


    ballots = [
    Ballot(ranking=(0, 1), tally=0),
    Ballot(ranking=(1, 2), tally=2),
    Ballot(ranking=(2, 1), tally=11)
]
    result, no_ties = kemeny_young(ballots)
    print(f"Winner: {result}, No ties: {no_ties}")
    

if __name__ == "__main__":
    main()