import logging
import data.day_3_wires

def parse_dir(c):
    d = {
        'U': (0, 1), 
        'D': (0, -1), 
        'L': (-1, 0), 
        'R': (1, 0)}
    return d.get(c)

def add_coords(a, b):
    return (a[0] + b[0], a[1] + b[1])

def wire_to_coords(wire):
    loc = (0,0)
    res = [loc]
    for w in wire:
        offset, n = parse_dir(w[0]), int(w[1:]) 
        for _ in range(n):
            loc = add_coords(loc, offset)
            res.append(loc)
    return res

def parse_coords_from_input(in_str):
    wires = in_str.split('\n')
    parse_wire = lambda x: wire_to_coords(x.split(','))
    w1, w2 = map(parse_wire, wires)
    return w1, w2

def manhattan_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_intersections(w1, w2):
    intersections =  set(w1) & set(w2)
    intersections.remove((0,0))
    return intersections

def get_closest_intersection_distance(w1, w2):
    intersections = get_intersections(w1, w2)

    get_dist = lambda x: manhattan_dist((0,0), x)
    d = [(x, get_dist(x)) for x in intersections]
    closest = sorted(d, key = lambda x: x[1])[0]
    return closest[1]

def get_steps_to_point(wire, point):
    for i, x in enumerate(wire):
        if x == point:
            return i
    logging.error("Point not found!")


def get_least_steps_intersection(w1, w2):
    intersections = get_intersections(w1, w2)
    calculate_steps = lambda x: get_steps_to_point(w1, x) + get_steps_to_point(w2, x)
    steps = [(i, calculate_steps(i)) for i in intersections]
    closest = sorted(steps, key = lambda x: x[1])[0]
    return closest[1]

if __name__ == "__main__":
    in_wires = data.day_3_wires.in_wires

    w1, w2 = parse_coords_from_input(in_wires)

    # Part 1
    print("Part 1 answer: ", get_closest_intersection_distance(w1, w2))

    # Part 2
    print("Part 2 answer: ", get_least_steps_intersection(w1, w2))


