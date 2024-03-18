from collections import defaultdict
from typing import Dict, List, Tuple, Hashable, Optional
import typing

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


def save_position(ballots: List[Ballot], candidates: set[Hashable]) -> Dict[Hashable, List[Hashable]]:
    num_candidates: int = len(candidates)
    positions: Dict[Hashable, List[Hashable]] = {candidate: [] for ballot in ballots for candidate in ballot.ranking}
    for ballot in ballots:
        missing_cadidates: set[Hashable] = candidates ^ set(ballot.ranking)
        for i in range(ballot.tally):
            count: int = 0
            for position, candidate in enumerate(ballot.ranking):
                positions[candidate].append(position)
                positions[candidate].sort()
                count += 1
            if len(missing_cadidates) != 0:
                num = 0
                for j in range(count, num_candidates):
                    num += j
                avg = num / len(missing_cadidates)
                for c in missing_cadidates:
                    if c not in positions:
                        positions[c] = []
                    positions[c].append(avg)
                    positions[c].sort()
    return positions


def calculate_median_rank(positions: List[Hashable]) -> float:
    print("INSIDE MEDIAN RANK: ", positions)
    sorted_positions: List[Hashable]= sorted(positions)
    length = len(sorted_positions)
    if length % 2 == 0:
        return (sorted_positions[length//2 - 1] + sorted_positions[length//2]) / 2
    else:
        return sorted_positions[length//2]
    

def topmost_median_rank(ballots: List[Ballot]) -> Result:
    print(ballots[1].ranking)
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)
    positions: Dict[Hashable, List[Hashable]] = save_position(ballots, candidates)
    print("POSITIONS: ", positions)
    median_ranks: Dict[Hashable, Hashable] = {candidate: calculate_median_rank(sorted(positions[candidate])) for candidate in positions}
    print("MEDIAN RANKS: ", median_ranks)
    min_median_rank = min(median_ranks.values())
    finalists = [candidate for candidate, rank in median_ranks.items() if rank == min_median_rank]
    print("FINALISTS: ", finalists)

    if len(finalists) == 1:
        return finalists[0], True
    else:
        winners: List[Hashable | None] = typical_judgement(median_ranks, finalists, positions)
        return winners[0], len(winners) == 1

def typical_judgement(median_ranks: Dict[Hashable, Hashable], finalists: List[Hashable], positions: Dict[Hashable, List[Hashable]]) -> List[Hashable | None]:
    max_diff = float('-inf')
    winners = []
    differences = {}
    for candidate in finalists:
        if candidate not in differences:
            differences[candidate] = 0
        proponents = 0
        opponents = 0
        lst = sorted(positions[candidate])
        median_val = median_ranks[candidate]
        for c in lst:
            if c < median_val:  # Proponent
                proponents += 1
            elif c > median_val:  # Opponent
                opponents += 1
        diff = proponents - opponents
        differences[candidate] = diff 
        if diff > max_diff:
            max_diff = diff
            winners = [candidate]
        elif diff == max_diff:
            winners.append(candidate)
    
    return winners

scheme: Scheme = topmost_median_rank
name: str = "topmost_median_rank"


def main() -> None:
    # shared_main(name, scheme)
    ballots = [Ballot(ranking=(1,2), tally=6),
    Ballot(ranking=(2,), tally=2),
    Ballot(ranking=(2,), tally=4)]
    result, no_ties = topmost_median_rank(ballots)
    print(f"Winner: {result}, No ties: {no_ties}")


if __name__ == "__main__":
    main()