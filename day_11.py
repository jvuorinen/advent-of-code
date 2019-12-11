import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from collections import defaultdict

from common import read_input
from computer import Computer
import numpy as np

TURNING_LOOKUP = {
    ('UP', 0): 'LEFT',
    ('LEFT', 0): 'DOWN',
    ('DOWN', 0): 'RIGHT',
    ('RIGHT', 0): 'UP',
    ('UP', 1): 'RIGHT',
    ('LEFT', 1): 'UP',
    ('DOWN', 1): 'LEFT',
    ('RIGHT', 1): 'DOWN'
}

DIRECTION_OFFSETS = {
    'UP':(0,1),
    'DOWN': (0,-1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

def get_next_direction(current, which_way):
    return TURNING_LOOKUP[(current, which_way)]

def get_direction_offset(direction):
    return DIRECTION_OFFSETS[direction]

def get_new_loc(current_loc, direction_to_go):
    offset = get_direction_offset(direction_to_go)
    return (current_loc[0] + offset[0], current_loc[1] + offset[1])


class HullColorMap:
    def __init__(self):
        self.painted = defaultdict(list)
        self.default_color = 0

    def get_color(self, loc):
        c = self.painted.get(loc, [self.default_color])
        return c[-1]

    def paint(self, loc, color):
        self.painted[loc].append(color)

    def visualize(self):
        # Get final colors of cells
        # Shift coords to be all positive
        x_coords, y_coords = zip(*(x for x in self.painted.keys()))
        x_shift, y_shift = abs(min(x_coords)), abs(min(y_coords))
        white_cells = [(c[0] + x_shift, c[1] + y_shift) for c, l in self.painted.items() if l[-1]==1]
        
        # Create a numpy array and make the painting
        # Note how x and y are represented in a np array
        x_max, y_max = map(max, zip(*white_cells))
        a = np.zeros(shape=(y_max + 1, x_max + 1))
        for x, y in white_cells:
            a[y_max - y, x] = 1

        # Print the array
        conversion = {0: "░", 1: "▓"}
        l = a.tolist()
        print("\n".join(["".join(map(conversion.get, row)) for row in l]))

        

class PainterRobot:
    def __init__(self, program):
        self.loc = (0,0)
        self.direction = 'UP'
        self.brain = Computer(program)
        self.brain.run()
        self.map = HullColorMap()

    def __repr__(self):
        return f"Painting robot at {self.loc} facing {self.direction}\nComputer state:\n{self.brain}"

    def step(self):
        # First paint
        current_color = self.map.get_color(self.loc)

        logging.info(f"Robo standing on {self.loc}, current plate color: {current_color}")

        self.brain.add_input(current_color)
        self.brain.run()

        new_color, which_way = self.brain.state.outputs[-2:]

        self.map.paint(self.loc, new_color)
        logging.info(f"Painted the cell at {self.loc} to color {new_color}")
        
        # Then turn
        self.direction = get_next_direction(self.direction, which_way)
        logging.info(f"Turned to face {self.direction}")

        # Then move
        new_loc = get_new_loc(self.loc, self.direction)
        logging.info(f"Moved from {self.loc} to {new_loc}")
        self.loc = new_loc

    def paint_all(self):
        while self.brain.status != "FINISHED":
            self.step()


if __name__ == "__main__":
    logging.getLogger().setLevel("WARNING")

    raw_in = read_input('data/day_11.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    # Part 1
    robot = PainterRobot(program)
    robot.paint_all()
    robot.map.visualize()

    n_painted_at_least_once = len(robot.map.painted)
    print(f"Step 1 answer: {n_painted_at_least_once}")

    # Part 2
    robot = PainterRobot(program)
    robot.map.paint((0,0), 1)
    robot.paint_all()
    robot.map.visualize()