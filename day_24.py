import logging
logging.basicConfig(format='%(levelname)s %(message)s')

from common import *

SIZE = 5
POINTS = np.array([2**i for i in range(SIZE**2)])

def get_neighbors(a, c):
    tmp = (c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)
    return [a[c] for c in tmp]

def get_updated_area(area):
    a = area.copy()
    maxlen = SIZE + 1

    for i in range(1, maxlen):
        for j in range(1, maxlen):
            neighbors = get_neighbors(area, (i, j)) 
            n_bugs = len([n for n in neighbors if n == ord('#')])

            if (area[i, j] == ord('.')) & (n_bugs in (1, 2)):
                a[i, j] = ord('#')
            elif (area[i, j] == ord('#')) & (n_bugs != 1):
                a[i, j] = ord('.')               
            else:
                a[i, j] = area[i, j] 
    return a


def get_rating(area):
    maxlen = SIZE + 1
    bugs = area[1:maxlen, 1:maxlen].flatten() == ord('#')

    total = sum(bugs * POINTS)
    return total


def solve_1(area):
    a = area.copy()
    ratings = {get_rating(area)}

    i = 0
    while True:
        i+= 1
        if i % 100_000 == 0:
            logging.info(f"On iteration {i:,}")
        a = get_updated_area(a)
        s = get_rating(a)
        if s in ratings:
            logging.info(f"Step 1 answer: {s} (iteration {i:,})")            
            return i
            # break
        else:
            ratings.add(s)


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    raw_in = read_input('data/day_24.txt')
    area = str_to_array(raw_in)
    
    solve_1(area)

