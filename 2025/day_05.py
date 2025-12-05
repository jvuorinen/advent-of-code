from itertools import chain
from utils import read, print_answers


def count(range):
    return max(0, range[1] - range[0] + 1)


def remove_overlap(r1, r2):
    overlaps = [(max(r1[1] + 1, r2[0]), r2[1]), (r2[0], min(r1[0] - 1, r2[1]))]
    return [x for x in overlaps if count(x) > 0]


def part2(ranges):
    ranges = ranges.copy()
    cleaned = []
    while ranges:
        r = ranges.pop()
        cleaned.append(r)
        ranges = list(chain(*[remove_overlap(r, x) for x in ranges]))
    return sum(map(count, cleaned))


a, b = read(2025, 5).split("\n\n")

ranges = [tuple(map(int, x.split("-"))) for x in a.split("\n")]
ids = list(map(int, b.split("\n")))

a1 = sum([any([r[0] <= x <= r[1] for r in ranges]) for x in ids])
a2 = part2(ranges)

print_answers(a1, a2, day=5)
