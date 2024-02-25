from collections import Counter
from typing import Dict, Hashable, List

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main

def irv(ballots: List[Ballot]) -> Result:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)
    total_votes: int = sum(ballot.tally for ballot in ballots)
    majority: float = total_votes / 2
    round: int = 1
    eliminated_candidates: set[Hashable] = set()
    while True:
        first_choice_votes: Dict[Hashable, int] = {}
        # counting first choice votes
        for ballot in ballots:
            if len(ballot.ranking) != 0:  
                for i in range(len(ballot.ranking)):
                    if ballot.ranking[i] in eliminated_candidates:
                        continue
                    if ballot.ranking[i] not in first_choice_votes:
                        first_choice_votes[ballot.ranking[i]] = 0
                    first_choice_votes[ballot.ranking[i]] += ballot.tally
                    break
        
        missing_cadidates: set[Hashable] = candidates ^ first_choice_votes.keys()
        # print("CANDIDATES: ", candidates, "| MAJORITY: ",majority,  "| FCV: ", first_choice_votes, "ROUND:", round)

        # Check for a majority winner
        for candidate, votes in first_choice_votes.items():
            if votes > majority:
                return candidate, True  # True indicates a single winner
            if len(first_choice_votes.keys()) == 1:
                return candidate, True
        
        if len(missing_cadidates) > 1 and round == 1:
            return -2, False
        
        if round == 1:
            for c in missing_cadidates:
                first_choice_votes[c] = 0
            
        # return None, False

       
            
        count: int = 0

        for candidate, votes in first_choice_votes.items():
            if votes == min(first_choice_votes.values()):
                eliminated_candidates.add(candidate)
                count += 1
        

        if count > 1:
            return None, False
        
        round += 1

scheme: Scheme = irv
name: str = "irv"



def main() -> None:
    shared_main("irv", scheme)


    # ballots = [   Ballot(ranking=(2, 1), tally=2),
    # Ballot(ranking=(3, 4), tally=3),
    # Ballot(ranking=(0, 3), tally=0),
    # Ballot(ranking=(4, 2), tally=5),
    # Ballot(ranking=(3, 0), tally=3)]
    # result, no_ties = irv(ballots)
    # print(f"Winner: {result}, No ties: {no_ties}")


if __name__ == "__main__":
    main()
