from collections import Counter
from typing import Dict, Hashable, List

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


def irv(ballots: List[Ballot]) -> Result:
    total_votes: int = sum(ballot.tally for ballot in ballots)
    majority: float = total_votes / 2
    round: int = 1
    candidate_not_found = True
    eliminated_candidates: List[Hashable] = []
    while candidate_not_found:
        first_choice_votes: Dict[Hashable, int] = {}

        # counting first choice votes
        for ballot in ballots:
            if len(ballot.ranking) != 0:  
                for i in range(len(ballot.ranking)):
                    if ballot.ranking[i] in eliminated_candidates:
                        continue
                    if ballot.ranking[i] not in first_choice_votes:
                        first_choice_votes[ballot.ranking[i]] = 0
                    # print("ADDINGS {} points to {}".format(ballot.tally, ballot.ranking[i]))
                    first_choice_votes[ballot.ranking[i]] += ballot.tally
                    break

        print("MAJORITY: ",majority,  "| FCV: ", first_choice_votes)


        # Check for a majority winner
        for candidate, votes in first_choice_votes.items():
            if votes > majority:
                return candidate, True  # True indicates a single winner
            if len(first_choice_votes) == 1:
                return candidate, True
            
        count: int = 0
        for candidate, votes in first_choice_votes.items():
            if votes == min(first_choice_votes.values()):
                eliminated_candidates.append(candidate)
                count += 1
        if count > 1:
            return None, False
        # print("ELIM CAND: ", eliminated_candidates)
        # If all remaining candidates have the same number of votes, it's a tie
        # if len(first_choice_votes) == len(eliminated_candidates):
        #     return -2, False  # False indicates a tie

        # Eliminate the candidate(s) and remove them from the ballots
        # for ballot in ballots:
        #     ballot.ranking = [candidate for candidate in ballot.ranking if candidate not in eliminated_candidates]

        round += 1
    return -3, False

scheme: Scheme = irv
name: str = "irv"



def main() -> None:
    shared_main("irv", scheme)
    # ballot1 = Ballot((1,2), 2)
    # ballot2 = Ballot((2,0), 0)
    # ballot3 = Ballot((2,1), 11)

    # ballots = [   Ballot(ranking=(1, 2), tally=6),
    # Ballot(ranking=(2, 1), tally=8),
    # Ballot(ranking=(4, 5), tally=8),
    # Ballot(ranking=(0, 5), tally=6),
    # Ballot(ranking=(1, 3), tally=13)]
    # result, no_ties = irv(ballots)
    # print(f"Winner: {result}, No ties: {no_ties}")


if __name__ == "__main__":
    main()
