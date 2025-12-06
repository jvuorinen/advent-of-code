from itertools import groupby
from utils import read, print_answers

*nums, ops = read(2025, 6).split("\n")
ops = ops.split()

g1 = list(zip(*map(str.split, nums)))

joined = ["".join(x).strip() for x in zip(*nums)]
g2 = [list(g) for k, g in groupby(joined, lambda x: x != "") if k]

a1 = sum(eval(op.join(g)) for g, op in zip(g1, ops))
a2 = sum(eval(op.join(g)) for g, op in zip(g2, ops))

print_answers(a1, a2, day=6)
