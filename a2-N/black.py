from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Hashable, Optional

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


def borda(candidates: set[Hashable], ballots: list[Ballot]) -> Result:
    size: int = max(len(ballot.ranking) for ballot in ballots)
    points: list[int] = [c for c in range(size - 1, -1, -1)]
    scores: Counter[Hashable] = Counter()
    for ballot in ballots:
        # candidates_used: set[Hashable] = set()
        for i, candidate in enumerate(ballot.ranking):
            # candidates_used.add(candidate)
            scores[candidate] += points[i] * ballot.tally
        # missing_cadidates: set[Hashable] = candidates ^ candidates_used
        # for c in candidates_used:
        #     for c2 in missing_cadidates:
        #        scores[c] += ballot.tally

    max_score: int = max(scores.values())
    winners: list[Hashable] = [
        candidate for candidate, score in scores.items() if score == max_score
    ]

    # print("BORDA SCORES: ", scores)

    # print("BORDA WINNERS: ", winners)
    return winners[0], len(winners) == 1


def black(ballots: List[Ballot]) -> Result:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)
    matrix: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2} for c1 in candidates}
    pairwise_matrix: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2} for c1 in candidates}

    # Step 1: Collect all candidates and count pairwise preferences
    for ballot in ballots:
        candidates_used: set[Hashable] = set()
        for i, candidate_a in enumerate(ballot.ranking):
            candidates_used.add(candidate_a)
            for candidate_b in ballot.ranking[i + 1:]:
                matrix[candidate_a][candidate_b] += ballot.tally
                candidates_used.add(candidate_b)
        missing_cadidates: set[Hashable] = candidates ^ candidates_used
        # # print("MISSING CANDIDATES: ", missing_cadidates)
        for c in candidates_used:
            for c2 in missing_cadidates:
                matrix[c][c2] += ballot.tally
    
    # print("MATRIX: ", matrix)

    #  pairwise matrix
    for candidate, dict1 in matrix.items():
        for candidate2, win_by in dict1.items():
            pairwise_matrix[candidate][candidate2] =  dict1[candidate2] - matrix[candidate2][candidate]

    print("PAIRWISE MATRIX: ", pairwise_matrix)
    condorcet_winners = []

    for c1 in candidates:
        wins_against_all = all(pairwise_matrix[c1][c2] > 0 for c2 in candidates if c1 != c2)
        if wins_against_all:
            condorcet_winners.append(c1)
    # print(condorcet_winners)
    if condorcet_winners:
        # print("CONDORCET WINNER FOUND!")
        return condorcet_winners[0], len(condorcet_winners) == 1
    
    # print("DOING BORDA!")
    return borda(candidates, ballots)
   


scheme: Scheme = black
name: str = "black"


def main() -> None:
    # shared_main(name, scheme)
    ballots = [   Ballot(ranking=(1, 0), tally=6),
    Ballot(ranking=(0, 2), tally=8),
    Ballot(ranking=(1, 2), tally=2),
    Ballot(ranking=(2, 1), tally=5)]
    result, no_ties = black(ballots)
    print(f"Winner: {result}, No ties: {no_ties}")


if __name__ == "__main__":
    main()