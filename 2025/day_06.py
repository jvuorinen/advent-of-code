from itertools import groupby
from utils import read, print_answers

raw = read(2025, 6).split("\n")

a1 = sum(eval(op.join(ns)) for *ns, op in zip(*map(str.split, raw)))

tmp = [n if not (n := "".join(x)).isspace() else None for x in zip(*raw[:-1])]
groups = [list(g) for k, g in groupby(tmp, lambda x: x is None) if not k]
ops = raw[-1].split()
a2 = sum(eval(op.join(g)) for g, op in zip(groups, ops))

print_answers(a1, a2, day=6)