from typing import Dict, Hashable, Tuple, Union

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main

def copeland(ballots: list[Ballot]) -> Result:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)
    matrix: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2} for c1 in candidates}

    for ballot in ballots:
        candidates_used: set[Hashable] = set()
        for i, candidate_a in enumerate(ballot.ranking):
            candidates_used.add(candidate_a)
            for candidate_b in ballot.ranking[i + 1:]:
                matrix[candidate_a][candidate_b] += ballot.tally
                candidates_used.add(candidate_b)
        missing_cadidates: set[Hashable] = candidates ^ candidates_used
        # print("MISSING CANDIDATES: ", missing_cadidates)
        for c in candidates_used:
            for c2 in missing_cadidates:
                matrix[c][c2] += ballot.tally

    # print(matrix)
    result, no_ties = copeland_winner(matrix)
    return result, no_ties

def copeland_winner(matrix: dict[Hashable, dict[Hashable, int]]) -> Result:
    # print(matrix)
    copeland_scores: Dict[Hashable, float] = {}
    comparisons: set[Tuple[Hashable, Hashable]] = set()
    for candidate, dict1 in matrix.items():
        if candidate not in copeland_scores:
            copeland_scores[candidate] = 0
        for candidate2, win_by in dict1.items():
            if candidate2 not in copeland_scores:
                copeland_scores[candidate2] = 0
            if (candidate, candidate2) not in comparisons:
                if win_by > matrix[candidate2][candidate]:
                    copeland_scores[candidate] +=1
                elif win_by < matrix[candidate2][candidate]:
                    copeland_scores[candidate2] +=1
                else:
                    copeland_scores[candidate] += 0.5
                    copeland_scores[candidate2] += 0.5
            comparisons.add((candidate,candidate2))
            comparisons.add((candidate2,candidate))
        



    winners = [candidate for candidate, score in copeland_scores.items() if score == max(copeland_scores.values())]
    # print("WINNERS LIST: ", winners)
    # print(copeland_scores)

    if winners:
        return winners[0], len(winners) == 1 
    else:
        return None, True

scheme: Scheme = copeland
name: str = "copeland"


def main() -> None:
    shared_main("copeland", scheme)
    ballots = [  Ballot(ranking=(4, 2, 0, 3), tally=4),
    Ballot(ranking=(2, 1), tally=3),
    Ballot(ranking=(3, 4, 0, 1, 2), tally=2),
    Ballot(ranking=(0, 3), tally=4),
    Ballot(ranking=(3, 2, 4), tally=2),
    Ballot(ranking=(4, 0, 2), tally=6)]
    result, no_ties = copeland(ballots)
    print(f"Winner: {result}, No ties: {no_ties}")


if __name__ == "__main__":
    main()