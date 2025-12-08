from itertools import combinations
from math import prod
from utils import read, print_answers

raw = read(2025, 8).split("\n")

boxes = [tuple(map(int, x.split(','))) for x in raw]
pairs = sorted(
    combinations(boxes, 2),
    key=lambda pair: sum([(a-b)**2 for a, b in zip(*pair)])
)
circuits = [{x} for x in boxes]

a2 = None
for i, (a, b) in enumerate(pairs, 1):
    join = []
    for c in circuits:
        if (a in c) ^ (b in c):
            join.append(c)
    if len(join) == 2:
        circuits.remove(join[0])
        circuits.remove(join[1])
        circuits.append(set.union(*join))
    if not a2 and len(circuits) == 1:
        a2 = a[0] * b[0]
        break
    if i == 1000:
        a1 = prod(sorted(map(len, circuits))[-3:])

print_answers(a1, a2, day=8)
