from collections import Counter
from typing import Dict, Hashable, List

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main

def bucklin(ballots: List[Ballot]) -> Result:
    size: int = max(len(ballot.ranking) for ballot in ballots)
    scores = {}

    for round_num in range(size):
        for ballot in ballots:
            if round_num < len(ballot.ranking):
                candidate = ballot.ranking[round_num]
                # print(candidate)
                if candidate not in scores:
                    scores[candidate] = 0
                scores[candidate] +=  ballot.tally
        # print("Round {}: {}".format(round_num+1, scores))
        max_votes: int = max(scores.values(), default=0)
        winners: List[Hashable] = [
            candidate for candidate, votes in scores.items() if votes == max_votes
        ]
        # checking if the max votes is greater than majority
        if max_votes > sum(ballot.tally for ballot in ballots) // 2: 
            return winners[0], len(winners) == 1  # if there are multiple winners
        # if the candidate with the highest votes still don't reach majority votes by the last round, return the candidate w the highest votes
        elif round_num == size - 1: 
            return winners[0], len(winners) == 1 
    
    return None, False

scheme: Scheme = bucklin
name: str = "bucklin"


def main() -> None:
    shared_main(name, scheme)


    # ballots = [   Ballot(ranking=(2, 1), tally=2),
    # Ballot(ranking=(3, 4), tally=3),
    # Ballot(ranking=(0, 3), tally=0),
    # Ballot(ranking=(4, 2), tally=5),
    # Ballot(ranking=(3, 0), tally=3)]
    # result, no_ties = irv(ballots)
    # print(f"Winner: {result}, No ties: {no_ties}")


if __name__ == "__main__":
    main()
