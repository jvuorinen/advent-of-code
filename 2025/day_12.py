from math import prod
from utils import read, print_answers

raw = read(2025, 12).split("\n\n")

todo = []
for line in raw[-1].split("\n"):
    a, b = line.split(': ')
    todo.append((tuple(map(int, a.split('x'))), tuple(map(int, b.split(' ')))))

a1 = sum([(prod(a) - sum(9*x for x in b)) >= 0 for a, b in todo])
a2 = None

print_answers(a1, a2, day=12)