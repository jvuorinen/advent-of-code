import logging
from functools import reduce
from itertools import cycle, islice
from operator import add
from functools import lru_cache

import numpy as np

from common import read_input

logging.basicConfig(format='%(levelname)s %(message)s')

@lru_cache(maxsize=None)
def deal_with_increment(length, n):
    idxes = list(range(length))
    new_one = idxes.copy()
    loop = islice(cycle(range(length)), 0, None, n)

    for i in range(len(deck)):
        idxes[next(loop)] = new_one[i]

    return np.array(idxes)

@lru_cache(maxsize=None)
def cut(length, n):
    idxes = list(range(length))
    idxes = idxes[n:] + idxes[:n]
    return np.array(idxes)


@lru_cache(maxsize=None)
def deal_into_new_stack(length):
    idxes = list(range(length))[::-1]
    return np.array(idxes)

def solve_1(deck, commands):
    length = len(deck)
    d = deck.copy()

    for c in commands:
        logging.debug("-----------------------------------")
        logging.debug(d)
        words = c.split(' ')
        if (words[0] == 'deal') & (words[1] == 'with'):
            n = int(words[-1])
            logging.debug(f"Deal with inc {n}")
            idxes = deal_with_increment(length, n)
        elif (words[0] == 'deal') & (words[1] == 'into'):
            logging.debug(f"Dealing into new stack")
            idxes = deal_into_new_stack(length)
        elif words[0] == 'cut':
            n = int(words[-1])
            logging.debug(f"Cutting {n}")
            idxes = cut(length, n)

        logging.debug(idxes)
        d = d[idxes]
        logging.debug(d)  
    print(f"Step 1 answer: {np.where(d==2019)[0][0]}")      
    return d

if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    commands = read_input('data/day_22.txt')

    # Step 1
    deck = np.arange(10007)
    %time d = solve_1(deck, commands)
    