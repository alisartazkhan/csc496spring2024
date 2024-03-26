from collections import defaultdict
from typing import Dict, List, Tuple, Hashable, Optional, Set
import typing

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main


from collections import defaultdict
from typing import List, Dict, Hashable, Set, Any, Tuple



def schulze(ballots: List[Ballot]) -> Result:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)

    def initialize_pairwise_matrix() -> Dict[Hashable, Dict[Hashable, int]]:
        return defaultdict(lambda: defaultdict(int))

    def initialize_paths() -> Dict[Hashable, Dict[Hashable, int]]:
        return defaultdict(lambda: defaultdict(int))

    def initialize_graph() -> Dict[Hashable, Dict[Hashable, int]]:
        return defaultdict(lambda: defaultdict(int))

    losers: Set[Hashable] = set()


   
    matrix: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2} for c1 in candidates}
    pairwise_matrix: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2} for c1 in candidates}

    # Step 1: Collect all candidates and count pairwise preferences
    for ballot in ballots:
        candidates_used: set[Hashable] = set()
        for i, candidate_a in enumerate(ballot.ranking):
            candidates_used.add(candidate_a)
            for candidate_b in ballot.ranking[i + 1:]:
                matrix[candidate_a][candidate_b] += ballot.tally
                candidates_used.add(candidate_b)
        missing_cadidates: set[Hashable] = candidates ^ candidates_used
        # # print("MISSING CANDIDATES: ", missing_cadidates)
        for c in candidates_used:
            for c2 in missing_cadidates:
                matrix[c][c2] += ballot.tally
    print("MATRIX: ", matrix)

    #  pairwise matrix
    for candidate, dict1 in matrix.items():
        for candidate2, win_by in dict1.items():
            c1_beats_c2 = win_by
            c2_beats_c1 = matrix[candidate2][candidate]
            if c1_beats_c2 > c2_beats_c1:
                pairwise_matrix[candidate][candidate2] =  c1_beats_c2

    print("PAIRWISE MATRIX: ", pairwise_matrix)
    paths: Dict[Hashable, Dict[Hashable, int]] =  {c1: {c2: 0 for c2 in candidates if c1 != c2} for c1 in candidates}

    for c1 in candidates:
        for c2 in candidates:
            if c1 == c2:
                continue
            if pairwise_matrix[c1][c2] > pairwise_matrix[c2][c1]:
                paths[c1][c2] = pairwise_matrix[c1][c2]
            else:
                paths[c1][c2] = 0
    print("PATHS :", paths)
    graph: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2} for c1 in candidates}
    for c1 in candidates:
        for c2 in candidates:
            # if sum(paths[c2].values()) == 0:
            #     losers.add(c2)
            if c1 != c2:
                if paths[c1][c2] > paths[c2][c1]:
                    graph[c1][c2] = paths[c1][c2]
    print("DIRECTED G: ", graph)
    for c1 in candidates:
        for c2 in candidates:
            if c2 in losers and c1 != c2:
                paths[c1][c2] = 1
            elif c1 != c2:
                paths[c1][c2] = find_strongest_path(c1, c2, graph, None, set())
    print("STRONGEST PATHS: ", paths)

    print("AFTER REMOVING NONE: ", paths)

    winning_candidates: Dict[Hashable, Dict[Hashable, int]] = {c1: {c2: 0 for c2 in candidates if c1 != c2} for c1 in candidates}
    for c1 in candidates:
        for c2 in candidates:
            if c1 != c2:
                c1_beats_c2 = paths[c1][c2]
                c2_beats_c1 = paths[c2][c1]
                if c1_beats_c2 > c2_beats_c1:
                    winning_candidates[c1][c2] = 1
                else:
                    winning_candidates[c1][c2] = 0

    most_wins_c: Dict[Hashable, int] = {}
    for c in candidates:
        most_wins_c[c] = sum(winning_candidates[c].values())

    most_wins: int = max(most_wins_c.values())
    winners: List[Hashable] = [candidate for candidate in candidates if most_wins_c[candidate] == most_wins]
    print("WINNERS: ", winners)
    if winners:
        return winners[0], len(winners) == 1
    else:
        return "<AMBIGUOUS>", False

def find_strongest_path(start: Hashable, end: Hashable, graph: Dict[Hashable, Dict[Hashable, int]],
                        min_strength: Any,
                        visited: Set[Hashable]) -> int:
    if start == end:
        return min_strength
    if start not in graph or start in visited:
        return 0

    visited.add(start)
    all_strengths: List[int] = []

    max_edge_strength: int = max(graph[start].values())

    for n in graph[start]:
        strength = graph[start][n]
        if n not in visited:
            new_strength: int = min(min_strength, strength) if min_strength is not None else strength
            path_strength: int = find_strongest_path(n, end, graph, new_strength, visited)
            if path_strength > 0:
                all_strengths.append(path_strength)

    visited.remove(start)
    
    if len(all_strengths) != 0:
        return max(all_strengths) 
    else:
        return 0

scheme: Scheme = schulze
name: str = "schulze"

def main() -> None:
    # shared_main(name, scheme)
    ballots = [   Ballot(ranking=(0, 1), tally=8),
    Ballot(ranking=(0, 2), tally=5)]
    result, no_ties = schulze(ballots)
    print(f"Winner: {result}, No ties: {no_ties}")
    # one = Node(1)
    # two = Node(2)
    # three = Node(3)

    # one.add_child(two)
    # two.add_child(three)
    # three.add_child(one)
    # # print(one)
    # # print(two)
    # # print(three)


if __name__ == "__main__":
    main()