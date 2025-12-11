from itertools import combinations, permutations, product, count, cycle
from functools import reduce, cache
from collections import Counter, defaultdict, deque
from math import prod
import numpy as np
from re import findall
import networkx as nx
from tqdm import tqdm
from utils import read, print_answers

# raw = read().split("\n")
raw = read(2025, 11).split("\n")

G = {}
for line in raw:
    a, b = line.split(': ')
    G[a] = b.split(' ')


def crawl(node, end, cnt = 0, path = None):
    path = path or []
    if node == end:
        return 1
    return sum( crawl(n, end, cnt, path) for n in G.get(node, []))

crawl("you", "out")

crawl("dac", "out")
crawl("fft", "out")



a1 = len(tally["paths"])
a2 = len([x for x in tally["paths"] if "dac" in ])

print_answers(a1, a2, day=11)
