from collections import defaultdict
from typing import Dict, List, Tuple, Hashable, Optional

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


def river(ballots: List[Ballot]) -> Result:
    pairwise_preferences: Dict[Tuple[Hashable, Hashable], int] = defaultdict(int)
    candidates: List[Hashable] = []

    # Step 1: Collect all candidates and count pairwise preferences
    for ballot in ballots:
        for i, higher_ranked_candidate in enumerate(ballot.ranking):
            if higher_ranked_candidate not in candidates:
                candidates.append(higher_ranked_candidate)
            for lower_ranked_candidate in ballot.ranking[i + 1:]:
                pairwise_preferences[(higher_ranked_candidate, lower_ranked_candidate)] += ballot.tally

    # Step 2: Determine the winner based on pairwise preferences
    while True:
        river_graph: Dict[Hashable, List[Hashable]] = {candidate: [] for candidate in candidates}
        for (winner, loser), tally in pairwise_preferences.items():
            river_graph[winner].append(loser)

        # Try to find a Condorcet winner
        condorcet_winner: Optional[Hashable] = None
        for candidate in candidates:
            if all(candidate in river_graph[loser] for loser in candidates if loser != candidate):
                condorcet_winner = candidate
                break

        if condorcet_winner is not None:
            return condorcet_winner, True  # True indicates a single winner

        # Identify and break the smallest margin in the cycle
        weakest_link: Optional[Tuple[Hashable, Hashable]] = None
        smallest_margin: int = float('inf')
        for (winner, loser), tally in pairwise_preferences.items():
            if loser in river_graph[winner] and tally < smallest_margin:
                smallest_margin = tally
                weakest_link = (winner, loser)

        if weakest_link is None:
            # This scenario implies a tie or an error in logic
            return "<AMBIGUOUS>", False

        # Remove the weakest link to break the cycle
        del pairwise_preferences[weakest_link]


scheme: Scheme = river
name: str = "river"


def main() -> None:
    shared_main(name, scheme)


if __name__ == "__main__":
    main()