import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from string import ascii_letters

from common import *

def str_to_array(raw_in):
    as_list = [list(l) for l in raw_in]
    tmp = [list(map(ord, l)) for l in as_list]
    return np.array(tmp)

def draw(a):
    CHARS = {n: chr(n) for n in range(256)}
    print_array(a, CHARS)

def find_symbol(symbol, a):
    tmp = np.where(a == ord(symbol))
    if sum(sum(tmp)) > 0:
        if len(tmp[0]) > 1:
            return [tuple(t) for t in np.where(a == ord(symbol))]
        else:
            return [(tmp[0][0], tmp[1][0])]


def create_teleport_dict(area):
    pairs = {}
    for c in ascii_letters:
        locs = find_symbol(c, area)
        try:
            if len(locs) >= 2:
                pairs[c] = locs
        except:
            pass
    return pairs


def get_unfilled_neighbors(c, a):
    tmp = (c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)
    return set([c for c in tmp if a[c] not in (ord('#'), ord(' '))])



def solve_1(area):
    a = area.copy()
    td = create_teleport_dict(area)

    start = find_symbol('A', area)[0]

    frontier = {start}
    fill_symbol = " "

    i = -1
    a[start] = ord('.')
    while len(frontier) > 0:
        next_round = frontier.copy()
        for c in frontier:
            next_round -= {c}
            code = a[c]
            if code == ord('.'):
                next_round |= get_unfilled_neighbors(c, a) # Get next round neighbors
            elif code == ord('Z'):
                print(f"Part 1 answer: {i-1}")

            a[c] = ord(fill_symbol) # Fill
        frontier = next_round
        i += 1

    draw(a)


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    raw_in = read_input('data/day_20.txt')

    area = str_to_array(raw_in)
    draw(area)

    

