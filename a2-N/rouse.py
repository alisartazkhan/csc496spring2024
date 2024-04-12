from collections import Counter
from typing import Dict, Hashable, List

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main

def borda(ballots: list[Ballot], candidates) -> Counter[Hashable]:
    size: int = 0

    for ballot in ballots:
        s: int = 0
        for c in ballot.ranking:
            if c in candidates:
                s += 1
        if s > size:
            size = s
    size = len(candidates)
    scores: Counter[Hashable] = Counter()
    for ballot in ballots:
        j = 0
        points: list[int] = [c for c in range(size, 0, -1)]
        missing_candidates = set(candidates) ^ set(ballot.ranking)
        for i, candidate in enumerate(ballot.ranking):
            if candidate in candidates:
                scores[candidate] += points[j] * ballot.tally
                j += 1
        l = 0
        for c in missing_candidates:
            if c in candidates:
                l +=  1
        if l != 0:
            avg = 1/l
            for c in missing_candidates:
                if c in candidates:
                    scores[c] += avg * ballot.tally
        print(scores)
    return scores
    max_score: int = max(scores.values())
    winners: list[Hashable] = [
        candidate for candidate, score in scores.items() if score == max_score
    ]
    return winners[0], len(winners) == 1

def find_strongest_candidate(scores, candidates):
    max_score = max(scores.values())
    tied_candidates = [candidate for candidate in candidates if scores[candidate] == max_score]
    if len(tied_candidates) > 1:
        return None
    return tied_candidates[0]

def find_weakest_candidate(scores, candidates):
    max_score = min(scores.values())
    tied_candidates = [candidate for candidate in candidates if scores[candidate] == max_score]
    if len(tied_candidates) > 1:
        return None
    return tied_candidates[0]

def rouse(ballots: List[Ballot]) -> Result:
    candidates = list({candidate for ballot in ballots for candidate in ballot.ranking})

    while len(candidates) > 2:
        scores = borda(ballots, candidates)
        print("SCORES1", scores)
        strongest = find_strongest_candidate(scores, candidates)
        if strongest == None:
            return 0, False
        temp_candidates = [c for c in candidates if c != strongest]
        temp_scores = borda(ballots, temp_candidates)
        print("TEMP SCORES", temp_scores)  # Using the same function to find the weakest

        weakest = find_weakest_candidate(temp_scores, temp_candidates)
        if weakest == None:
            return 0, False
        candidates.remove(weakest)
        print("REMOVED", weakest)
    
    final_scores = borda(ballots, candidates)
    print(final_scores)
    winner = find_strongest_candidate(final_scores, candidates)
    return winner, winner != None

scheme: Scheme = rouse
name: str = "rouse"



def main() -> None:
    # shared_main("rouse", scheme)


    ballots = [   
    Ballot(ranking=(0, 1), tally=7),
    Ballot(ranking=(1, 2), tally=1),
    Ballot(ranking=(2, 1), tally=5)
    ]
    result, no_ties = rouse(ballots)
    print(f"Winner: {result}, No ties: {no_ties}")


if __name__ == "__main__":
    main()
