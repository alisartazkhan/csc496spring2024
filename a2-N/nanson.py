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

        print("ELIMINATED CANDIDATES: ", eliminated_candidates)
        candidates = candidates.difference(eliminated_candidates)
        
        if len(candidates) == 0:
            return None, False
        size: int = len(candidates)

        print("CANDIDATES: ", candidates, "SIZE: ", size)
        if len(candidates) == 1:
            return list(candidates)[0], True

        points: list[int] = [c for c in range(size, 0, -1)]
        print("POINTS: ", points)

        scores: Counter[Hashable] = Counter()

        for ballot in ballots:
            i = 0
            for candidate in ballot.ranking:
                if candidate not in eliminated_candidates:
                    scores[candidate] += points[i] * ballot.tally
                    print("{}points*{}tally = {} goes to {} for ballot: {} | Scores: {}".format(points[i], ballot.tally, points[i]*ballot.tally, candidate, ballot.ranking, scores))                                                     
                    i += 1

        size = len(scores.keys())
        # if size == 0:
        #     print(ballots)
        avg: float = sum(scores.values()) / size

        
        print("SCORES: ", scores, "AVG: ", avg )
        winners: list[Hashable] = []
        count: int = 0
        for candidate, score in scores.items():
            if len(scores.keys()) == 1:
                winners.append(candidate)
            if score <= avg:
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
    # ballots: List[Ballot] = [Ballot(ranking=("W"), tally=5141), 
    # Ballot(ranking=("W", 'A', 'N'), tally=4281),
    # Ballot(ranking=('J'), tally=3925),
    # Ballot(ranking=('A'), tally=3195),
    # Ballot(ranking=('J', 'A', 'N'), tally=2446),
    # Ballot(ranking=('A', 'W', 'N'), tally=2237),
    # Ballot(ranking=('W', 'A'), tally=1734),
    # Ballot(ranking=('A', 'N', 'W'), tally=1422),
    # Ballot(ranking=('A', 'J', 'N'), tally=1275),
    # Ballot(ranking=('A', 'W'), tally=997)]

    # result, no_ties = nanson(ballots)
    # print(f"Winner: {result}, No ties: {no_ties}")

Expected: 0
Got: 2
{ "ballots": [
{ "count":  8, "ranking": [0, 2] },
{ "count":  4, "ranking": [1, 2] },
{ "count":  1, "ranking": [2, 0] }],
"winners": {"baldwin?": "<AMBIGUOUS>", "black": 0, "borda": 0, "bucklin": 0, "bucklin?": 0, "copeland": 0, "dodgson": 0, "irv": 0, "nanson": 0, "nanson?": 0, "river": "<AMBIGUOUS>", "river?": "<AMBIGUOUS>", "schulze": 0, "smith_irv": 0, "topmost_median_rank": 1} }

if __name__ == "__main__":
    main()