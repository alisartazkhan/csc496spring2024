from common.types import Ballot, Result, Scheme

from irv import irv
from copeland import copeland


# Example usage:
# ballot1 = Ballot((0,1), 8)
# ballot2 = Ballot((0,2), 5)
# ballots = [ballot1, ballot2]
# "winners": {"black": 0, "borda": 0, "copeland": 0, "irv": 0, "river": "<AMBIGUOUS>"} },

# ballot1 = Ballot((1,2), 2)
# ballot2 = Ballot((2,0), 0)
# ballot3 = Ballot((2,1), 11)
# ballots = [ballot1, ballot2, ballot3]
# "winners": {"black": 2, "borda": 2, "copeland": 2, "irv": 2, "river": "<AMBIGUOUS>"} },


# ballot1 = Ballot((0, 1), 3)
# ballot2 = Ballot((0, 2), 9)
# ballot3 = Ballot((1, 2), 0)
# ballot4 = Ballot((2, 1), 1)
# ballots = [ballot1, ballot2, ballot3, ballot4]
# "winners": {"black": 0, "borda": 0, "copeland": 0, "irv": 0, "river": "<AMBIGUOUS>"} },


# ballot1 = Ballot((0, 2), 4)
# ballot2 = Ballot((2, 1), 9)
# ballots = [ballot1, ballot2]
# "winners": {"black": 2, "borda": 2, "copeland": 2, "irv": 2, "river": "<AMBIGUOUS>"} },


# ballot1 = Ballot((1, 0), 3)
# ballot2 = Ballot((1, 2), 8)
# ballot3 = Ballot((2, 1), 2)
# ballots = [ballot1, ballot2, ballot3]
# "winners": {"black": 1, "borda": 1, "copeland": 1, "irv": 1, "river": "<AMBIGUOUS>"} },

ballot1 = Ballot((3,0,2,1), 10)
ballot2 = Ballot((2,3,1,0), 6)
ballot3 = Ballot((0,2,1,3), 11)
ballot4 = Ballot((1,3,0,2), 15)
ballots = [ballot1, ballot2, ballot3, ballot4]
# 3 is supposed to be the winner

# ballot1 = Ballot(("A" , "E" , "C" , "D" , "B"), 31)
# ballot2 = Ballot(("B" , "A" , "E"), 30)
# ballot3 = Ballot(("C" , "D" , "B"), 29)
# ballot4 = Ballot(("D" , "A" , "E"), 10)
# ballots = [ballot1, ballot2, ballot3, ballot4]
# A is supposed to win

result, no_ties = copeland(ballots)
print(f"Winner: {result}, No ties: {no_ties}")