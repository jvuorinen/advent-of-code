import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from itertools import repeat, chain, islice, cycle

from common import read_input


def process(n, n_phases):
    phase = lambda i: islice(cycle(chain.from_iterable(l for l in zip(*repeat([0, -1, 0, 1], i)))), 1, None, 1)

    for _ in range(n_phases):
        n = [int(str(sum(a*b for a, b in zip(n, phase(i))))[-1]) for i in range(1, len(n)+1)]

    return "".join(map(str, n))[:8]



if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    raw_in = [int(c) for c in read_input('data/day_16.txt')[0]]

    # Step 1
    print(f"Step 1 answer: {process(raw_in, 100)}")

    # # Step 2
    # real = raw_in * 100
    # process(int(real))