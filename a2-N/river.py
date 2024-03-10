from collections import defaultdict
from typing import Dict, List, Tuple, Hashable, Optional
import typing

from common.types import Ballot, Result, Scheme
from common.shared_main import shared_main



class Node:
    def __init__(self, value: Hashable):
        self.value: Hashable = value
        self.parent: Optional['Node'] = None
        self.next: List['Node'] = []

    def __str__(self) -> str:
        parent_value = self.parent.value if self.parent else "None"
        children_values = [child.value for child in self.next]
        return f"{parent_value} -> {self.value} -> {children_values}"
    
    def is_valid(self, child: 'Node') -> bool:
        if child.parent is not None:
            # # print("Error: Child node has multiple parents.")
            return False

        # Create the child node and set its parent
        child.parent = self
        self.next.append(child)


        # # Check for cycles
        visited: List[Hashable] = []
        q: List['Node'] = [self]  # Use a queue for BFS
        while len(q) != 0:
            current_node = q.pop(0)
            if current_node.value in visited:
                # # print("ERROR: Creating a cycle in the graph.")
                child.parent = None
                self.next.remove(child)
                return False

            visited.append(current_node.value)
            # # print("CURRENT: ", current_node.value, "VISITED: ", visited)

            q.extend(current_node.next)

        child.parent = None
        self.next.remove(child)
        return True
    

    def add_child(self, child: 'Node') -> Optional['Node']:
        # # print(f"\n\nADDING CHILD: {self.value} -> {child.value}")
        # Check if the child node already has a parent
        if child.parent is not None:
            # # print("Error: Child node has multiple parents.")
            return None

        # Create the child node and set its parent
        child.parent = self
        self.next.append(child)


        # # Check for cycles
        visited: List[Hashable] = []
        q: List['Node'] = [self]  # Use a queue for BFS
        while len(q) != 0:
            current_node = q.pop(0)
            if current_node.value in visited:
                # # print("ERROR: Creating a cycle in the graph.")
                child.parent = None
                self.next.remove(child)
                return None

            visited.append(current_node.value)
            # # print("CURRENT: ", current_node.value, "VISITED: ", visited)

            q.extend(current_node.next)

       
        return child



def river(ballots: List[Ballot]) -> Result:
    candidates: set[Hashable] = set(candidate for ballot in ballots for candidate in ballot.ranking)
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

    print("PAIRWISE PREF: ", matrix)

    #  pairwise matrix
    for candidate, dict1 in matrix.items():
        for candidate2, win_by in dict1.items():
            pairwise_matrix[candidate][candidate2] =  dict1[candidate2] - matrix[candidate2][candidate]

    print("PAIRWISE MATRIX: ", pairwise_matrix)
    # Flatten the nested dictionary values
    all_values = [(key1, key2, value) for key1, inner_dict in pairwise_matrix.items() for key2, value in inner_dict.items()]
    nodes: Dict[Hashable, Node] = {}
    while len(all_values) != 0:
        # Find the maximum value
        max_value = max(all_values, key=lambda x: x[2])[2]

        if max_value < 0:
            break
        # print(all_values)
        # Find all keys associated with the maximum value
        max_keys = [(key1, key2, value) for key1, key2, value in all_values if value == max_value]
        # print(max_keys)

        
        can_add: bool = True
        valid_pairs: List[Tuple] = []
        for pairings in max_keys:
            parent: Hashable = pairings[0]
            if parent not in nodes:
                nodes[parent] = Node(parent)
            child: Hashable = pairings[1]
            if child not in nodes:
                nodes[child] = Node(child)
            print(max_keys)
            if can_add and nodes[parent].is_valid(nodes[child]):
                valid_pairs.append(pairings)
                # nodes[parent].add_child(nodes[child])
                can_add = False
            elif can_add != True and nodes[parent].is_valid(nodes[child]):
                return "<AMBIGUOUS>", False 
        
        parent = valid_pairs[0][0]
        if parent not in nodes:
            nodes[parent] = Node(parent)
        child = valid_pairs[0][1]
        if child not in nodes:
            nodes[child] = Node(child)
        
        nodes[parent].add_child(nodes[child])

            

        # # print(max_keys)


        # Remove processed keys from all_values
        all_values = [(key1, key2, value) for key1, key2, value in all_values if (key1, key2, value) not in max_keys]


    for val, node in nodes.items():
        winner: Node = find_winner(node)
        break
    # # print("ALL VALUES: ", all_values)
    # # print("MAX VALUES: ", max_keys)
    return winner.value, True

def find_winner(node: Node) -> Node:
    cur: Node = node
    # # print(cur)

    while cur.parent is not None:
        cur = cur.parent

    return cur

scheme: Scheme = river
name: str = "river"


def main() -> None:
    shared_main(name, scheme)
    # ballots = [Ballot(ranking=(0, 2), tally=4),
    #         Ballot(ranking=(2, 1), tally=9)]
    # result, no_ties = river(ballots)
    # print(f"Winner: {result}, No ties: {no_ties}")
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