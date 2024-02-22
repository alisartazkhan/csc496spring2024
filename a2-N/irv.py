
from collections import Counter
from typing import Hashable

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main

def irv(ballots: list[Ballot]) -> Result:
    remaining_candidates = set(candidate for ballot in ballots for candidate in ballot.ranking)
    
    while len(remaining_candidates) > 1:
        scores = {}
        
        for ballot in ballots:
            for candidate in ballot.ranking:
                if candidate in remaining_candidates:
                    scores[candidate] = scores.get(candidate, 0) + ballot.tally
                    break  # Break once the first valid candidate is found in the ranking
        
        min_votes = min(scores.values(), default=float('inf'))
        losers = [candidate for candidate, votes in scores.items() if votes == min_votes]
        
        for loser in losers:
            remaining_candidates.remove(loser)
        
        # Check if any remaining candidate has more than half the total votes
        if max(scores.values(), default=0) > sum(ballot.tally for ballot in ballots) // 2:
            return max(scores, key=scores.get), True
    
    # If there is no clear winner, return the remaining candidate (or None if no candidate is left)
    return remaining_candidates.pop() if remaining_candidates else None, False


scheme: Scheme = irv
name: str = "irv"


def main() -> None:
    shared_main("irv", scheme)


if __name__ == "__main__":
    main()