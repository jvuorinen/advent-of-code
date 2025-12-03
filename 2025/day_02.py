from re import findall
from utils import read, print_answers

ranges = [tuple(map(int, x.split("-"))) for x in read(2025, 2).split(",")]

a1 = a2 = 0
for a, b in ranges:
    for n in range(int(a), int(b) + 1):
        a1 += n if findall(r"^(\d+)\1$", str(n)) else 0
        a2 += n if findall(r"^(\d+)\1+$", str(n)) else 0

print_answers(a1, a2, day=2)
