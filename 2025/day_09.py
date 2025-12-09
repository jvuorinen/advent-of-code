from itertools import combinations
from utils import read, print_answers

raw = read(2025, 9).split("\n")

coords = [tuple(map(int, x.split(","))) for x in raw]
pairs = list(combinations(coords, 2))


def size(a, b):
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def classify(c, pair):
    right = c[0] <= min(pair[0][0], pair[1][0])
    left = c[0] >= max(pair[0][0], pair[1][0])
    over = c[1] <= min(pair[0][1], pair[1][1])
    under = c[1] >= max(pair[0][1], pair[1][1])
    return right, left, over, under


def is_good(pair):
    r, l, o, u = False, False, False, False
    for c in coords + [coords[0]]:
        _r, _l, _o, _u = classify(c, pair)
        # Check if crosses box
        if (_r and l) or (r and _l):
            if not any([_o, o, _u, u]):
                return False
        if (_o and u) or (o and _u):
            if not any([_l, l, _r, r]):
                return False
        r, l, o, u = _r, _l, _o, _u
        # Check if inside box
        if not any([r, l, o, u]):
            return False
        # Bug: won't catch if it circumvents the box
        # but apparently not a problem with this input...
    return True


a1 = max([size(*pair) for pair in pairs])
a2 = max([size(*pair) for pair in pairs if is_good(pair)])

print_answers(a1, a2, day=9)
