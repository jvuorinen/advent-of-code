import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from itertools import islice
import os
from random import sample

import numpy as np

from common import read_input
from computer import Computer

DIR_OFFSETS = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0),
}


def getchar():
   #Returns a single character from standard input
   import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch


class Map:
    def __init__(self):
        self.coords = {}
        self.start = (0,0)
        self.distance = {(0,0): 0}

    def render(self, bot_loc):
        # Shift coords to avoid negatives
        x_shift = abs(min(i[0] for i in self.coords.keys()))
        y_shift = abs(min(i[1] for i in self.coords.keys()))
        
        cells = {(k[0] + x_shift, k[1] + y_shift): v for k, v in self.coords.items()}

        # Create a numpy array from coordinate information
        # Note how x and y are represented in a np array
        x_max, y_max = map(max, zip(*cells.keys()))
        a = np.empty(shape=(y_max + 1, x_max + 1)).astype(int)
        a[:] = -1
        for (x, y), v in cells.items():
            a[y_max - y, x] = v

        # Update bot loc and start loc
        a[y_max - (bot_loc[1] + y_shift), bot_loc[0] + x_shift] = 3
        a[y_max - (self.start[1] + y_shift), self.start[0] + x_shift] = 4

        # Print the array
        conversion = {-1: " ", 0:"▓", 1: "░", 2:"€", 3:"@", 4:"S"}
        l = a.tolist()
        for line in l:
            print("|" + "".join(conversion.get(t, " ") for t in line))


class RepairBot:
    def __init__(self, program):
        self.brain = Computer(program)
        self.brain.run()
        self.loc = (0,0)
        self.map = Map()
        self.map.coords[self.loc] = 1

    def __repr__(self):
        return f"I am a robot at {self.loc}"

    def reset(self):
        self.brain.reset()
        self.brain.run()
        self.loc = (0,0)

    def step(self, i):
        offset = DIR_OFFSETS.get(i)
        attempted_loc = (self.loc[0] + offset[0], self.loc[1] + offset[1])
        logging.info(f"Attempting to move from {self.loc} to {attempted_loc}")

        self.brain.add_input(i)
        self.brain.run()
        o = self.brain.state.outputs.pop()

        if o == 0:
            logging.info("Hit a wall!")
            self.map.coords[attempted_loc] = 0
        elif o == 1:
            logging.info("Cell is ok, moved there")
            self.map.coords[attempted_loc] = 1

            attempted_distance = self.map.distance.get(attempted_loc, None)
            if attempted_distance is None:
                current_dist = self.map.distance[self.loc]
                self.map.distance[attempted_loc] = current_dist + 1

            self.loc = attempted_loc

        elif o == 2:

            self.map.coords[attempted_loc] = 2

            attempted_distance = self.map.distance.get(attempted_loc, None)
            if attempted_distance is None:
                current_dist = self.map.distance[self.loc]
                self.map.distance[attempted_loc] = current_dist + 1
            
            logging.info(f"FOUND IT AT DISTANCE: {attempted_distance}")

            self.loc = attempted_loc           

    def run(self):
        i = 0 
        while True:
            i+= 1
            if i > 1000000: 
                # Failsafe
                break

            self.map.render(self.loc)
            print(f"At {self.loc}, distance: {self.map.distance[self.loc]}")


            user_input = getchar()
            # Clear console
            os.system('cls' if os.name == 'nt' else 'clear') 

            if user_input == "q":
                break
            
            elif user_input == "i":
                self.step(1)

            elif user_input == "k":
                self.step(2)

            elif user_input == "j":
                self.step(3)

            elif user_input == "l":
                self.step(4)


def make_array(coords):
    """Makes a np array out of coodinates"""
    # Shift coords to avoid negatives
    x_shift = abs(min(i[0] for i in coords.keys()))
    y_shift = abs(min(i[1] for i in coords.keys()))
    
    cells = {(k[0] + x_shift, k[1] + y_shift): v for k, v in coords.items()}

    # Create a numpy array from coordinate information
    # Note how x and y are represented in a np array
    x_max, y_max = map(max, zip(*cells.keys()))
    a = np.empty(shape=(y_max + 1, x_max + 1)).astype(int)
    a[:] = -1
    for (x, y), v in cells.items():
        a[y_max - y, x] = v

    return a


def print_array(a, conversion):
    l = a.tolist()
    for line in l:
        print("|" + "".join(conversion.get(t, " ") for t in line))


def solve_step_2(map_coords):
    a = make_array(map_coords)

    conversion = {-1: " ", 0:"▓", 1: "░", 2:"€", 3:"@", 4:"S"}
    print_array(a, conversion)



if __name__ == "__main__":
    logging.getLogger().setLevel("WARNING")

    raw_in = read_input('data/day_15.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    bot = RepairBot(program)

    # Explore the map
    for i in range(500000):
        if i%1000 == 0:
            print(f"Iteration: {i}")
        move = sample([1,2,3,4],1)[0]
        bot.step(move)
    bot.map.render(bot.loc)

    # Step 2
    map_coords = bot.map.coords
    solve_step_2(map_coords)