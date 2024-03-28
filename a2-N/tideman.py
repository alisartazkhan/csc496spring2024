from collections import Counter
from typing import Dict, Hashable, List, Set

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


def copeland(ballots: list[Ballot]) -> List[Hashable]:
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
    winners: List[Hashable] = copeland_winner(matrix)

    return winners

def copeland_winner(matrix: dict[Hashable, dict[Hashable, int]]) -> List[Hashable]:
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

    return winners
def irv(ballots: List[Ballot], smith_set: Set[Hashable]) -> Set[Hashable] | None:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)
    total_votes: int = sum(ballot.tally for ballot in ballots)
    majority: float = total_votes / 2
    round: int = 1
    eliminated_candidates: set[Hashable] = candidates ^ smith_set

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
    print("CANDIDATES: ", candidates, "| FCV: ", first_choice_votes, "ROUND:", round)

    count: int = 0
    remove_from_ss = []
    for candidate, votes in first_choice_votes.items():
        if votes == min(first_choice_votes.values()):
            eliminated_candidates.add(candidate)
            remove_from_ss.append(candidate)
            count += 1
    

    if len(remove_from_ss) == 1:
        smith_set.remove(remove_from_ss[0])
    else:
        return None
    
    round += 1

    return smith_set

def compute_smith_set(ballots: List[Ballot], pairwise_matrix: Dict[Hashable, Dict[Hashable, int]]) -> Set[Hashable]:
    copeland_winners = copeland(ballots)

    smith_set = {copeland_winners[0]}

    while True:
        new_candidate_added = False
        for c1 in smith_set:
            for c2, winsBy in pairwise_matrix[c1].items():
                if winsBy < 0:
                    smith_set.add(c2)
                    new_candidate_added = True
        if not new_candidate_added:
            break

    # print("SMITH SET: ", smith_set)
    return smith_set


def make_matrix(ballots: list[Ballot], candidates: set[Hashable], eliminated_candidates: Set[Hashable]) -> Dict[Hashable, Dict[Hashable, int]]:
    matrix: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2 and c2 not in eliminated_candidates} for c1 in candidates if c1 not in eliminated_candidates}
    pairwise_matrix: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2 and c2 not in eliminated_candidates} for c1 in candidates if c1 not in eliminated_candidates}

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
    #  pairwise matrix
    for candidate, dict1 in matrix.items():
        for candidate2, win_by in dict1.items():
            pairwise_matrix[candidate][candidate2] =  dict1[candidate2] - matrix[candidate2][candidate]

    # print("PAIRWISE MATRIX: ", pairwise_matrix)
    return pairwise_matrix

def tideman(ballots: list[Ballot]) -> Result:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)
    eliminated_candidates: Set[Hashable] = set()
    pairwise_matrix: Dict[Hashable, Dict[Hashable, int]] = make_matrix(ballots, candidates, eliminated_candidates)
    print("MATRIX: ", pairwise_matrix)
    
    while True:
        smith_set:  Set[Hashable] = compute_smith_set(ballots, pairwise_matrix)
        print("SMITH SET: ", smith_set)
        if len(smith_set) == 1:
            return list(smith_set)[0], True
        smith_set = irv(ballots, smith_set)
        if len(smith_set) == 1:
            return list(smith_set)[0], True
        if smith_set == None:
            return 0, False
        




    return list(smith_set)[0], True

scheme: Scheme = tideman
name: str = "tideman"


def main() -> None:
    # shared_main(name, scheme)
    ballots = [  Ballot(ranking=(1,2), tally=2),
    Ballot(ranking=(2,0), tally=0),
    Ballot(ranking=(2,1), tally=11)]
    result, no_ties = tideman(ballots)
    print(f"Winner: {result}, No ties: {no_ties}")

if __name__ == "__main__":
    main()
