import logging

import pytest

from day_3 import parse_coords_from_input, get_closest_intersection_distance, get_least_steps_intersection

logging.getLogger().setLevel("DEBUG")


def test_1():
    raw_in = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
    w1, w2 = parse_coords_from_input(raw_in)

    d = get_closest_intersection_distance(w1, w2)
    assert d == 159


def test_2():
    raw_in = ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]
    w1, w2 = parse_coords_from_input(raw_in)

    d = get_closest_intersection_distance(w1, w2)
    assert d == 135

def test_3():
    raw_in = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
    w1, w2 = parse_coords_from_input(raw_in)

    d = get_least_steps_intersection(w1, w2)
    assert d == 610

def test_3():
    raw_in = ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]
    w1, w2 = parse_coords_from_input(raw_in)

    d = get_least_steps_intersection(w1, w2)
    assert d == 410