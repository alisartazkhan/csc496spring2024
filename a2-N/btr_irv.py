from collections import Counter
from typing import Dict, Hashable, Set

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


# def redistribute_ballots(ballots: list[Ballot], eliminated_candidates: Set[Hashable]):
#     for c in eliminated_candidates:
#         for ballot in ballots:
#             ballot.ranking = tuple(list(ballot.ranking).remove(c))
    
def bi(ballots: list[Ballot], candidates: Set[Hashable], eliminated_candidates: Set[Hashable]) -> list[Hashable]:
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
    # if len(missing_cadidates) == 1:
    #     first_choice_votes[list(missing_cadidates)[0]] = 0
    # elif len(missing_cadidates) > 1:
    #     return [-2, -2]

    # for c in missing_cadidates:
    #     first_choice_votes[c] = 0

    # Sort the first_choice_votes dictionary items by their values (vote counts)
    sorted_candidates = sorted(first_choice_votes.items(), key=lambda x: x[1])

    # Extract the two candidates with the fewest first-choice votes
    bottom_two_candidates = [candidate for candidate, _ in sorted_candidates[:2]]
    print("FCV: ", first_choice_votes)
    print("BOTTOM TWO: ", bottom_two_candidates)
    # print("CANDIDATES: ", candidates, "| MAJORITY: ",majority,  "| FCV: ", first_choice_votes, "ROUND:", round)

    return bottom_two_candidates

def make_matrix(ballots: list[Ballot], candidates: set[Hashable], eliminated_candidates: Set[Hashable]) -> Dict[Hashable, Dict[Hashable, int]]:
    matrix: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2 and c2 not in eliminated_candidates} for c1 in candidates if c1 not in eliminated_candidates}
    # Step 1: Collect all candidates and count pairwise preferences
    for ballot in ballots:
        candidates_used: set[Hashable] = set()
        for i, candidate_a in enumerate(ballot.ranking):
            if candidate_a not in eliminated_candidates:
                candidates_used.add(candidate_a)
                for candidate_b in ballot.ranking[i + 1:]:
                    if candidate_b not in eliminated_candidates:
                        matrix[candidate_a][candidate_b] += ballot.tally
                        candidates_used.add(candidate_b)
        missing_cadidates: set[Hashable] = candidates ^ candidates_used
        # # print("MISSING CANDIDATES: ", missing_cadidates)
        for c in candidates_used:
            for c2 in missing_cadidates:
                matrix[c][c2] += ballot.tally
        
    return matrix

    print("PAIRWISE PREF: ", matrix)
def btr_irv(ballots: list[Ballot]) -> Result:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)
    eliminated_candidates: Set[Hashable] = set()
    winners = candidates ^ eliminated_candidates
    matrix: Dict[Hashable, Dict[Hashable, int]] = make_matrix(ballots, candidates, eliminated_candidates)
    print(matrix)
    while len(winners) != 1:
        
        losers: list[Hashable] = bi(ballots, winners, eliminated_candidates)
        if len(losers) == 1:
            return losers[0], True
        a = losers[0]
        b = losers[1]
        if matrix[a][b] > matrix[b][a]:
            loser = b
        elif matrix[a][b] < matrix[b][a]:
            loser = a
        else:
            return 0, False
        eliminated_candidates.add(loser)
        # redistribute_ballots(ballots, eliminated_candidates)
        winners = candidates ^ eliminated_candidates
        print("WINNERS: ", winners)

    

    return list(winners)[0], True

scheme: Scheme = btr_irv
name: str = "btr_irv"


def main() -> None:
    # shared_main(name, scheme)
    ballots = [  Ballot(ranking=(0, 1), tally=8),
    Ballot(ranking=(0, 2), tally=5)]
    result, no_ties = btr_irv(ballots)
    print(f"Winner: {result}, No ties: {no_ties}")

if __name__ == "__main__":
    main()
