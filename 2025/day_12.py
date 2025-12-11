from itertools import combinations, permutations, product, count, cycle
from functools import reduce, cache
from collections import Counter, defaultdict, deque
from math import prod
import numpy as np
from re import findall
import networkx as nx
from tqdm import tqdm
from utils import read, print_answers

raw = read().split("\n")
# raw = read(2025, 12).split("\n")


a1 = None
a2 = None

print_answers(a1, a2, day=12)
