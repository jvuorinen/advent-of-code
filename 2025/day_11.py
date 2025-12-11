from functools import cache
from utils import read, print_answers

raw = read(2025, 11).split("\n")

G = {}
for line in raw:
    a, b = line.split(": ")
    G[a] = b.split(" ")

@cache
def count(node, end, cnt=0):
    return (node == end) or sum(count(n, end, cnt) for n in G.get(node, []))

a1 = count("you", "out")
a2 = sum([
    count("svr", "dac") * count("dac", "fft") * count("fft", "out"),
    count("svr", "fft") * count("fft", "dac") * count("dac", "out"),
])

print_answers(a1, a2, day=11)
