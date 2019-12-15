import logging
logging.basicConfig(format='%(levelname)s %(message)s')
import re
from itertools import combinations

import pandas as pd
import matplotlib.pyplot as plt

from common import read_input


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
        self.vel = Coordinate(0,0,0)

    def __repr__(self):
        return f"Position: {self.pos}, velocity: {self.vel}"

    def _step(self):
        new_pos = self.pos + self.vel
        # logging.debug(f"Moving from {self.pos} to {new_pos}")
        self.pos = new_pos

    def get_energy(self):
        potential = abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)
        kinetic = abs(self.vel.x) + abs(self.vel.y) + abs(self.vel.z)
        return potential * kinetic


def parse_bodies_from_str(txt_lines):
    parse_position = lambda txt: Coordinate(*re.findall(r"[-\d]+", txt))
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

    def simulate_and_draw_positions(self, n=150):
        idx, x_hist, y_hist, z_hist = [], [], [], [] 

        for _ in range(n):
            x_positions = [b.pos.x for b in self.bodies]
            y_positions = [b.pos.y for b in self.bodies]
            z_positions = [b.pos.z for b in self.bodies]

            idx.append(self.i)
            x_hist.append(x_positions)
            y_hist.append(x_positions)
            z_hist.append(x_positions)

            self._step()
            
        idx = [i for i in range(self.i-150, self.i)]
        df_x = pd.DataFrame(x_hist, columns=['A', 'B', 'C', 'D'], index = idx)
        df_y = pd.DataFrame(y_hist, columns=['A', 'B', 'C', 'D'], index = idx)
        df_z = pd.DataFrame(z_hist, columns=['A', 'B', 'C', 'D'], index = idx)

        df_x.plot()
        df_y.plot()
        df_z.plot()

    def _step(self):
        self.i += 1
        self._apply_gravitations()
        self._move_bodies()

    def _apply_gravitations(self):
        pairs = combinations(self.bodies, 2)
        for a, b in pairs:
            # logging.debug(f"Applying gravity for {a} and {b}")
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
            
            # logging.debug(f"Result {a} and {b}")

    def _move_bodies(self):
        for b in self.bodies:
            b._step()

    def get_energy(self):
        return sum(b.get_energy() for b in self.bodies)

    def find_stability_point(self):
        history = set(self._get_state_tuple())
        while True:
            if self.i % 100_000 == 0:
                logging.info(f"Finding stability point, iterations done {self.i}")
            self._step()
            state = self._get_state_tuple()
            if state in history:
                print(f"Stabilisation point found. System is stabilized after iteration {self.i - 1}")
                return 
            else:
                history.add(state)

    def _get_state_tuple(self):
        state_history = tuple([(b.pos.x, b.pos.y, b.pos.z, b.vel.x, b.vel.y, b.vel.z) for b in self.bodies])
        return state_history

if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    raw_in = read_input('data/day_12.txt')

    system = System(raw_in)

    # system.simulate_and_draw_positions()

    # Step 1
    # system.simulate(1000)
    # print(system)
    # print(system.get_energy())

    # system.find_stability_point()







