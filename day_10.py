import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from math import atan2

from common import read_input


def get_asteroid_coords(raw_in):
    l = []
    for i, line in enumerate(raw_in):
        for j, char in enumerate(line):
            if char == "#":
                l.append((i,j))
    return l


def get_angle(c1, c2):
    return atan2(c1[0] - c2[0], c1[1] - c2[1])


def solve_1(asteroids):
    n_visible = []
    for origin in asteroids:
        others = filter(lambda x: x != origin, asteroids)
        angles = [get_angle(origin, other) for other in others]
        n_visible.append(len(set(angles)))
    return max(n_visible)
            


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    raw_in = read_input('data/day_10.txt')
    asteroids = get_asteroid_coords(raw_in)

    print(f"Part 1 answer: {solve_1(asteroids)}")
    