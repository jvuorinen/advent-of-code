import logging
import operator
import re
from functools import reduce
from itertools import combinations

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from common import read_input

logging.basicConfig(format='%(levelname)s %(message)s')


class Coordinate:
    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, o):
        return Coordinate(self.x + o.x, self.y + o.y, self.z + o.z)


class BodyOfMass:
    def __init__(self, pos: Coordinate):
        self.pos = pos
        self.vel = Coordinate(0, 0, 0)

    def __repr__(self):
        return f"Position: {self.pos}, velocity: {self.vel}"

    def _step(self):
        new_pos = self.pos + self.vel
        self.pos = new_pos

    def get_potential_energy(self):
        potential = abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)
        return potential

    def get_kinetic_energy(self):
        kinetic = abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)
        return kinetic

    def get_energy(self):
        return self.get_kinetic_energy() * self.get_potential_energy()


def parse_bodies_from_str(txt_lines):
    def parse_position(txt): return Coordinate(*re.findall(r"[-\d]+", txt))
    bodies = [BodyOfMass(parse_position(txt)) for txt in txt_lines]
    return bodies


class System:
    def __init__(self, init_str):
        self.bodies = parse_bodies_from_str(init_str)
        self.i = 0

    def __repr__(self):
        bodies_str = "\n".join(map(str, self.bodies))
        return f"System of bodies\nIterations run: {self.i}\nBodies:\n" + bodies_str

    def simulate(self, steps):
        for _ in range(steps):
            self._step()

    def _step(self):
        self.i += 1
        self._apply_gravitations()
        self._move_bodies()

    def _apply_gravitations(self):
        pairs = combinations(self.bodies, 2)
        for a, b in pairs:
            x_a, x_b = a.pos.x, b.pos.x
            y_a, y_b = a.pos.y, b.pos.y
            z_a, z_b = a.pos.z, b.pos.z

            if x_a < x_b:
                a.vel.x += 1
                b.vel.x -= 1
            elif x_a > x_b:
                a.vel.x -= 1
                b.vel.x += 1

            if y_a < y_b:
                a.vel.y += 1
                b.vel.y -= 1
            elif y_a > y_b:
                a.vel.y -= 1
                b.vel.y += 1

            if z_a < z_b:
                a.vel.z += 1
                b.vel.z -= 1
            elif z_a > z_b:
                a.vel.z -= 1
                b.vel.z += 1

    def _move_bodies(self):
        for b in self.bodies:
            b._step()

    def get_energy(self):
        return sum(b.get_energy() for b in self.bodies)

    def find_stability_point(self):
        history = set(self._get_state_tuple())
        while True:
            if self.i % 100_000 == 0:
                logging.info(
                    f"Finding stability point, iterations done {self.i}")
            self._step()
            state = self._get_state_tuple()
            if state in history:
                print(
                    f"Stabilisation point found. System is stabilized after iteration {self.i - 1}")
                return
            else:
                history.add(state)

    def _get_state_tuple(self):
        state_history = tuple(
            [(b.pos.x, b.pos.y, b.pos.z, b.vel.x, b.vel.y, b.vel.z) for b in self.bodies])
        return state_history


def solve_1(raw_in):
    system = System(raw_in)
    system.simulate(1000)

    print(f"Step 1 answer: {system.get_energy()}")


def get_states(system):
    x_state = tuple((b.pos.x, b.vel.x) for b in system.bodies)
    y_state = tuple((b.pos.y, b.vel.y) for b in system.bodies)
    z_state = tuple((b.pos.z, b.vel.z) for b in system.bodies)
    return x_state, y_state, z_state


def solve_2(raw_in):
    system = System(raw_in)
    initial_x, initial_y, initial_z = get_states(system)

    i = 0
    x_stable, y_stable, z_stable = 0, 0, 0
    stabs_found = 0

    while True:
        i += 1
        system._step()
        state_x, state_y, state_z = get_states(system)

        if (x_stable == 0) & (state_x == initial_x):
            x_stable = i
            stabs_found += 1
        if (y_stable == 0) & (state_y == initial_y):
            y_stable = i
            stabs_found += 1
        if (z_stable == 0) & (state_z == initial_z):
            z_stable = i
            stabs_found += 1

        if stabs_found == 3:
            break
    
    lcm_1 = np.lcm(x_stable, y_stable)
    lcm_2 = np.lcm(lcm_1, z_stable)
    
    print(f"Step 2 answer: {lcm_2}")
    

if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    raw_in = read_input('data/day_12.txt')

    # Step 1
    solve_1(raw_in)

    # Step 2
    solve_2(raw_in)
