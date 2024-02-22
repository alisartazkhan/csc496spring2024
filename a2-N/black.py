from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Hashable, Optional

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


def black(ballots: List[Ballot]) -> Result:
    pairwise_preferences: Dict[Tuple[Hashable, Hashable], int] = defaultdict(int)
    borda_scores: Counter[Hashable] = Counter()
    candidates: List[Hashable] = []

    # Collect all candidates and initialize Borda scores
    for ballot in ballots:
        for candidate in ballot.ranking:
            if candidate not in candidates:
                candidates.append(candidate)
            borda_scores[candidate] += (len(candidates) - ballot.ranking.index(candidate) - 1) * ballot.tally

    # Count pairwise preferences
    for ballot in ballots:
        for i, higher_ranked_candidate in enumerate(ballot.ranking):
            for lower_ranked_candidate in ballot.ranking[i + 1:]:
                pairwise_preferences[(higher_ranked_candidate, lower_ranked_candidate)] += ballot.tally

    # Check for a Condorcet winner
    condorcet_winner: Optional[Hashable] = None
    for candidate in candidates:
        is_winner: bool = True
        for opponent in candidates:
            if candidate != opponent and pairwise_preferences.get((opponent, candidate), 0) >= pairwise_preferences.get((candidate, opponent), 0):
                is_winner = False
                break
        if is_winner:
            condorcet_winner = candidate
            break

    if condorcet_winner:
        return condorcet_winner, True  # True indicates a single winner

    # Use Borda count as a tie-breaker
    max_borda_score: int = max(borda_scores.values())
    borda_winners: List[Hashable] = [candidate for candidate, score in borda_scores.items() if score == max_borda_score]

    return borda_winners[0], len(borda_winners) == 1


scheme: Scheme = black
name: str = "Black"


def main() -> None:
    shared_main(name, scheme)


if __name__ == "__main__":
    main()