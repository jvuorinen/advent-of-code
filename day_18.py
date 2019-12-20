import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from string import ascii_lowercase, ascii_uppercase, ascii_letters
from collections import defaultdict

import numpy as np

from common import *



def str_to_array(raw_in):
    as_list = [list(l) for l in raw_in]
    tmp = [list(map(ord, l)) for l in as_list]
    return np.array(tmp)

def draw(a):
    CHARS = {n: chr(n) for n in range(256)}
    print_array(a, CHARS)

def find_symbol(symbol, a):
    x, y = map(lambda x:x[0], np.where(a == ord(symbol)))
    return x, y


def get_unfilled_neighbors(c, a):
    tmp = (c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)
    return set([c for c in tmp if a[c] not in (ord('#'), ord(' '))])


def get_distances(symbol, a):
    """Flood-fill algo to get distances from starting point"""
    a = a.copy()
    start = find_symbol(symbol, a)

    frontier = {start}
    i=-1
    fill_symbol = " "
    # letters = set(map(ord, ascii_letters))
    key_codes = set(map(ord, ascii_lowercase))
    door_codes = set(map(ord, ascii_uppercase))

    d = defaultdict(dict)

    a[start] = ord(fill_symbol)
    while sum(sum(a==ord('.'))) > 0:

        # Business logic
        keys = set()
        doors = set()
        # End business logic
        
        i += 1
        next_round = frontier.copy()
        for c in frontier:

            next_round -= {c}

            # Business logic here
            code = a[c]
            if code in key_codes:
                keys.add(chr(code))
            if code in door_codes:
                doors.add(chr(code))
            # End business logic

            a[c] = ord(fill_symbol) # Fill
            next_round |= get_unfilled_neighbors(c, a) # Get next round neighbors
            
        # Business logic here
        if (len(keys) > 0):
            d[i]['keys'] = keys
        if (len(doors) > 0):
            d[i]['doors'] = doors
        # End business logic

        frontier = next_round

    return dict(d)


def get_present_keys(a):
    all_chars_present = set([chr(x) for x  in np.unique(a)])
    key_characters = set(ascii_lowercase)
    return all_chars_present & key_characters
    

def build_distance_lookup(a):
    todo = list(get_present_keys(a)) + ['@']
    d = {c: get_distances(c, a) for c in todo}
    return d


def get_possibilities(loc, keys_found, distances):

    for k, v in distances[loc].items():
        print(k,v)
        doors = v.get('doors')
        if doors:
            print(k, doors)


class GameState:
    def __init__(self, id, loc, keys_found, steps, distances):
        self.id = id
        self.loc = loc
        self.keys_found = keys_found
        self.steps = steps
        self.distances = distances
        self.possibilities = get_possibilities(loc, keys_found)
    
    def __repr__(self):
        return f"st-{self.id}"



def solve_1(area):
    d = build_distance_lookup(area)

    draw(area)

    d['@']


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    raw_in = read_input('data/day_18.txt')
    area = str_to_array(raw_in)

    # Dev
    a = area.copy()
    loc = '@'
    keys_found=set()
    distances = build_distance_lookup(area)
