import logging
from functools import lru_cache, reduce
from itertools import cycle, islice
from operator import add

import numpy as np

from common import read_input

logging.basicConfig(format='%(levelname)s %(message)s')

# @lru_cache(maxsize=None)
def get_new_index(command, deck_size, idx):
    words = command.split(' ') 

    if (words[0] == 'deal') & (words[1] == 'with'):
        n = int(words[-1])
        tmp = (n * idx)
        
        return tmp - (int(tmp/deck_size)*deck_size)

    elif (words[0] == 'deal') & (words[1] == 'into'):
        return deck_size - 1 - idx

    elif words[0] == 'cut':
        n = int(words[-1])
        if n > 0:
            if idx <= (n - 1):
                return idx + (deck_size - n)
            else:
                return idx - n
        else:
            if idx <= (deck_size - 1 - abs(n)):
                return idx + abs(n)
            else:
                return idx - (deck_size - abs(n))


def solve_1(commands):
    idx = 2019
    deck_size = 10007

    for c in commands:
        idx = get_new_index(c, deck_size, idx)

    print(f"Part 1 answer: {idx}")


def solve_2(commands):
    idx = 2020
    deck_size = 101741582076661

    i = 0
    while True:
        i += 1
        if i%500_000 == 0:
            logging.info(f"On iteration {i:,}")
        for c in commands:
            idx = get_new_index(c, deck_size, idx)  
        if idx == 2020:
            return i




if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    commands = read_input('data/day_22.txt')

    solve_1(commands)

    # r = solve_2(commands)

