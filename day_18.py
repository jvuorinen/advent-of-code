import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from string import ascii_lowercase, ascii_uppercase, ascii_letters
from collections import defaultdict
from queue import PriorityQueue
from itertools import count
from functools import lru_cache

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


def get_distances(symbol, area):
    """Flood-fill algo to get distances from symbol point"""
    a = area.copy()

    start = find_symbol(symbol, a)
    frontier = {start}
    fill_symbol = " "
    node_codes = set([ord(c) for c in ascii_letters + '@1234'])
    i=-1
    d = {}
    a[start] = ord('.')

    while len(frontier) > 0:
        i += 1
        next_round = frontier.copy()
        for c in frontier:
            next_round -= {c}
            code = a[c]

            # Mark the distances
            if a[c] in node_codes:
                d[chr(code)] = i

            # Only explore the free nodes further
            if code == ord('.'):
                next_round |= get_unfilled_neighbors(c, a) # Get next round neighbors

            a[c] = ord(fill_symbol) # Fill
        frontier = next_round

    return d


def get_present_nodes(area):
    all_chars_present = set([chr(x) for x  in np.unique(area)])
    node_characters = set(ascii_letters + '@1234')
    return all_chars_present & node_characters
    

def build_distance_lookup(area):
    todo = list(get_present_nodes(area))
    d = {c: get_distances(c, area) for c in todo}
    return d

@lru_cache(maxsize = None)
def get_possibilities(loc, keys_found, distances):
    """Using Dijkstra's algorithm, get distances to all reachable keys"""
    INF = 9999

    keys = set(ascii_lowercase)
    reachable_doors = set([c for c in ascii_uppercase if c.lower() in keys_found])
    reachable = keys | reachable_doors | set('@1234')
    present_in_the_map = set(distances.keys()) 

    unvisited = reachable & present_in_the_map
    visited = set()

    tentative = {k: INF for k in present_in_the_map}
    tentative[loc] = 0
    current = loc

    while True:
        curr_d = tentative[current]
        neighbors = distances[current]

        for n, d in neighbors.items():
            if n not in visited:
                d_tmp = curr_d + d
                tentative[n] = min(tentative[n], d_tmp)

        unvisited.remove(current)
        visited.add(current)

        if len(unvisited) == 0:
            break

        current = min(unvisited, key=lambda x: tentative.get(x))

    final = {k: v for k, v in tentative.items() if (k not in keys_found) and (v != 9999) and (k in ascii_lowercase)}
    return final


# Need to make an immutable dict in order to make lru cache work
class HashableDict(dict):
    def __hash__(self):
        return hash(frozenset(self))


class GeneralInfo:
    def __init__(self, all_keys, distances):
        self.all_keys = frozenset(all_keys) 
        self.distances = HashableDict(distances)


class GameStateSingle:
    def __init__(self, loc, keys_found, steps, final, general_info):
        self.id = f"st-{loc}-{steps}-{keys_found}"
        self.loc = loc
        self.keys_found = keys_found
        self.steps = steps
        self.final = final
        self.possibilities = get_possibilities(loc, frozenset(keys_found), general_info.distances)
        self.general_info = general_info

    def __repr__(self):
        return self.id

    def step(self, key):
        """Returns the next game state if stepping on key"""
        next_keys = self.keys_found | {key}
        next_steps = self.steps + self.possibilities[key]
        final = (next_keys == self.general_info.all_keys)

        return GameStateSingle(key, next_keys, next_steps, final, self.general_info)
    

class GameStateMulti:
    def __init__(self, locs, keys_found, steps, final, general_info):
        self.id = f"st-{locs}-{steps}-{keys_found}"
        self.locs = locs
        self.keys_found = keys_found
        self.steps = steps
        self.final = final
        self.general_info = general_info
        self.possibilities = self._get_possibilities()
        self.steps_total = sum(self.steps)

    def __repr__(self):
        return self.id

    def step(self, action):
        """Returns the next game state if stepping on key"""
        robo, key, dist = action

        next_locs = list(self.locs)
        next_locs[robo] = key
        next_locs = tuple(next_locs)

        next_keys = self.keys_found | {key}

        next_steps = list(self.steps)
        next_steps[robo] += dist
        next_steps = tuple(next_steps)

        final = (next_keys == self.general_info.all_keys)

        new_state = GameStateMulti(
            next_locs, 
            next_keys, 
            next_steps, 
            final, 
            self.general_info)

        return new_state
    
    def _get_possibilities(self):
        p = []
        for i, loc in enumerate(self.locs):
            possibles = get_possibilities(
                loc, 
                frozenset(self.keys_found), 
                self.general_info.distances)
            if possibles:
                for k, v in possibles.items():
                    p.append((i, k, v))
        return tuple(p)


def solve_1(area):
    distances = build_distance_lookup(area)
    all_keys = set(ascii_lowercase) & get_present_nodes(area)
    general_info = GeneralInfo(all_keys, distances)

    first_state = GameStateSingle(
        loc = '@', 
        keys_found = set(), 
        steps = 0, 
        final = False,
        general_info = general_info)

    unvisited = [first_state]
    state_history = {} 
    shortest_final = 999999

    i = 0
    discarded = 0
    while unvisited:
        if i % 500_000 == 0:
            logging.info(f"Running... states explored {i:,}, states discarded: {discarded:,}, explore deck_size: {len(unvisited):,}, best so far: {shortest_final}")
        s = unvisited.pop()
        if s.final & (s.steps < shortest_final):
            shortest_final = s.steps

        for k in s.possibilities:
            new_state = s.step(k)
            new_state_str = f"{new_state.loc}-{new_state.keys_found}"
            best_so_far = state_history.get(new_state_str)
            if best_so_far:
                if new_state.steps < best_so_far:
                    unvisited.append(new_state)
                    state_history[new_state_str] = new_state.steps
                else:
                    discarded += 1
            else:
                unvisited.append(new_state)
                state_history[new_state_str] = new_state.steps
        i += 1

    print(f"All done")
    print(f"Shortest final: {shortest_final}")


def solve_2(area):
    area = area_2

    distances = build_distance_lookup(area)
    all_keys = set(ascii_lowercase) & get_present_nodes(area)
    general_info = GeneralInfo(all_keys, distances)

    first_state = GameStateMulti(
        locs = ('1', '2', '3', '4'), 
        keys_found = set(), 
        steps = (0,0,0,0), 
        final = False,
        general_info = general_info)

    unvisited = [first_state]
    state_history = {} 
    shortest_final = 999999

    i = 0
    discarded = 0
    while unvisited:
        if i % 500_000 == 0:
            logging.info(f"Running... states explored {i:,}, states discarded: {discarded:,}, explore deck_size: {len(unvisited):,}, best so far: {shortest_final}")
        s = unvisited.pop()
        if s.final & (s.steps_total < shortest_final):
            shortest_final = s.steps_total

        for a in s.possibilities:
            new_state = s.step(a)
            new_state_str = f"{new_state.locs}-{new_state.keys_found}"
            best_so_far = state_history.get(new_state_str)
            if best_so_far:
                if new_state.steps_total < best_so_far:
                    unvisited.append(new_state)
                    state_history[new_state_str] = new_state.steps_total
                else:
                    discarded += 1
            else:
                unvisited.append(new_state)
                state_history[new_state_str] = new_state.steps_total
        i += 1

    print(f"All done... states explored {i:,}, states discarded: {discarded:,}, explore deck_size: {len(unvisited):,}, best so far: {shortest_final}")
    print(f"Shortest final: {shortest_final}")




if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    raw_1 = read_input('data/day_18_1.txt')
    area_1 = str_to_array(raw_1)

    raw_2 = read_input('data/day_18_2.txt')
    area_2 = str_to_array(raw_2)

    # draw(area_1)
    # draw(area_2)

    # solve_1(area_1)
    # solve_2(area_2)