from utils import read, print_answers

raw = read(2025, 3).split("\n")


def turnon(line, left, v=""):
    if left == 0:
        return int(v)
    candidates = line[: (len(line) - left + 1)]
    best = max(candidates)
    ix = candidates.index(max(candidates))
    return turnon(line[ix + 1 :], left - 1, v + best)


a1 = sum([turnon(x, 2) for x in raw])
a2 = sum([turnon(x, 12) for x in raw])

print_answers(a1, a2, day=3)
