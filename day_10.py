import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from math import atan2, sqrt
from collections import defaultdict
from math import pi

from common import read_input


def get_asteroid_coords(raw_in):
    l = []
    for j, line in enumerate(raw_in):
        for i, char in enumerate(line):
            if char == "#":
                l.append((i,j))
    return l


def get_angle_and_distance(c1, c2):
    angle = atan2(c1[0] - c2[0], c1[1] - c2[1])
    distance = sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
    return angle, distance


def get_info(origin, asteroids):
    others = list(filter(lambda x: x != origin, asteroids))
    info_of_others = [get_angle_and_distance(origin, other) for other in others]

    info_dict = defaultdict(list)
    for coord, info in zip(others, info_of_others):
        info_dict[info[0]] += [(coord, info[1])]

    return info_dict
            

def rotate(f):
    if f > 0:
        f -= 2*pi
    return f
    

def sort_and_clean(info_dict):
    """Sorts info_dict to correct order for shooting"""
    d = dict(info_dict)
    d = {rotate(k): sorted(v, key=lambda x: x[1]) for k, v in d.items()}
    d = {k: v for k, v in sorted(d.items(), key=lambda item: item[0], reverse=True)}
    return d


def get_optimal_location(asteroids):
    l = []
    for a in asteroids:
        info = get_info(a, asteroids)
        n_visible = len(info)
        l.append((n_visible, a))
    best = max(l, key = lambda x: x[0])
    return best

def shoot_asteroids(station, asteroids):
    info_dict = get_info(station[1], asteroids)
    d = sort_and_clean(info_dict)

    i = 1
    while True:
        for k, v in d.items():
            if len(v) > 0:
                a = v[0]
                print(f"Number {i} asteroid to be vaporized is {a[0]}")
                i += 1
                d[k] = v[1:]
            if i == (len(asteroids)):
                return


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    raw_in = read_input('data/day_10.txt')
    asteroids = get_asteroid_coords(raw_in)

    station = get_optimal_location(asteroids)
    print(f"Part 1 answer: {station[0]}")

    shoot_asteroids(station, asteroids)