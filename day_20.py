import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from string import ascii_letters

from common import *

def draw(a):
    CHARS = {n: chr(n) for n in range(256)}
    print_array(a, CHARS)


def find_symbol(symbol, a):
    tmp = np.where(a == ord(symbol))
    if sum(sum(tmp)) > 0:
        if len(tmp[0]) > 1:
            return list(zip(*tmp))
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


def get_teleport_pair(symbol, loc, teleport_dict):
    print(f"Trying to get {symbol} from {loc}")
    both = teleport_dict.get(symbol)
    for i in both:
        if i != loc:
            return i

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
            else:
                pair = get_teleport_pair(chr(code), c, td)
                a[pair] = ord(fill_symbol) # Fill
                neighbors = get_unfilled_neighbors(pair, a)
                for n in neighbors:
                    next_round |= get_unfilled_neighbors(n, a) # Get next round neighbors
                    a[n] =  ord(fill_symbol)
            a[c] = ord(fill_symbol) # Fill
        frontier = next_round
        i += 1

    # draw(a)


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    raw_in = read_input('data/day_20.txt')

    area = str_to_array(raw_in)
    draw(area)

    solve_1(area)

    

