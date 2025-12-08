from itertools import combinations
from math import prod
from utils import read, print_answers

raw = read(2025, 8).split("\n")
boxes = [tuple(map(int, x.split(","))) for x in raw]
pairs = sorted(combinations(boxes, 2), key=lambda pair: sum([(a - b) ** 2 for a, b in zip(*pair)]))

circuits = {frozenset({x}) for x in boxes}
for i, (a, b) in enumerate(pairs, 1):
    join = {c for c in circuits if (a in c) ^ (b in c)}
    if join:
        circuits -= join
        circuits.add(frozenset.union(*join))
    if len(circuits) == 1:
        a2 = a[0] * b[0]
        break
    if i == 1000:
        a1 = prod(sorted(map(len, circuits))[-3:])

print_answers(a1, a2, day=8)
