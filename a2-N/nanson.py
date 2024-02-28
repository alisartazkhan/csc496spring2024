from collections import Counter
from typing import Dict, Hashable, List

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


def nanson(ballots: List[Ballot]) -> Result:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)

    eliminated_candidates: set[Hashable] = set()

    round: int = 0
    while True:
        print("\n\nROUND: ", round)

        print("ELIMINATED: ", eliminated_candidates)
        candidates = candidates.difference(eliminated_candidates)
        if len(candidates) == 1:
            return list(candidates)[0], True
        size: int = len(candidates)

        print("CANDIDATES: ", candidates, "SIZE: ", size)

        points: list[int] = [c for c in range(size, 0, -1)]
        print("POINTS: ", points)

        scores: Counter[Hashable] = Counter()

        for ballot in ballots:
            i = 0
            for candidate in ballot.ranking:
                if candidate not in eliminated_candidates:
                    scores[candidate] += points[i] * ballot.tally
                    print("{}*{} => {} for ballot: {} | Scores: {}".format(points[i], ballot.tally, candidate, ballot.ranking, scores))                                                     
                    i += 1

        size = len(scores.keys())
        avg: float = sum(scores.values()) / size
        
        print("SCORES: ", scores, "AVG: ", avg )
        winners: list[Hashable] = []
        count: int = 0
        for candidate, score in scores.items():
            if len(scores.keys()) == 1:
                winners.append(candidate)
            if score < avg:
                eliminated_candidates.add(candidate)
                count += 1
        
        if count == 0:
            return None, True

        if winners:
            return winners[0], len(winners) == 1
            
        round += 1
        

scheme: Scheme = nanson
name: str = "nanson"


def main() -> None:
    # shared_main(name, scheme)


    ballots: List[Ballot] = [Ballot(ranking=(0, 2), tally=8), 
    Ballot(ranking=(1, 2), tally=4), 
    Ballot(ranking=(2, 0), tally=1)]
    result, no_ties = nanson(ballots)
    print(f"Winner: {result}, No ties: {no_ties}")


if __name__ == "__main__":
    main()