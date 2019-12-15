import logging
logging.basicConfig(format='%(levelname)s %(message)s')
from itertools import islice
import os

import numpy as np

from common import *
from computer import Computer

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class ArcadeMachine:
    def __init__(self, program):
        self.computer = Computer(program, failsafe = 100_000_000, mem_size=10_000)
        self.score = 0
        # self.computer.run()

    def _render(self):
        """
        0 is an empty tile. No game object appears in this tile.
        1 is a wall tile. Walls are indestructible barriers.
        2 is a block tile. Blocks can be broken by the ball.
        3 is a horizontal paddle tile. The paddle is indestructible.
        4 is a ball tile. The ball moves diagonally and bounces off objects.
        """
        self.computer.run()
        outputs = self.computer.state.outputs
        self.computer.outputs = []

        xmax = max(islice(outputs, 0, None, 3))
        ymax = max(islice(outputs, 1, None, 3))
        
        screen = np.zeros((ymax + 1, xmax + 1), dtype = int)

        score = 0
        for chunk in chunks(outputs, 3):
            x, y, t = chunk
            screen[y, x] = t
            if (x, y) == (-1, 0):
                score = t

        # Clear console
        os.system('cls' if os.name == 'nt' else 'clear') 

        # Print the result
        conversion = {0: " ", 1: "▓", 2: "▒", 3: "▒", 4: "*"}
        l = screen.tolist()
        for line in l:
            print("".join(conversion.get(t, " ") for t in line))

        return score

    def play(self):
        # self.score = 0

        self.computer.state.mem[0] = 2 # Play without coins

        i = 0
        saves = []
        while True:
            self.score = self._render()
            print(f"Score: {self.score}")
            
            user_input = getchar()

            if user_input == "q":
                break

            elif user_input == "r":
                self.computer.reset()
                self.play()
            
            elif user_input == "z":
                try:        
                    score, state = saves.pop()
                    self.score = score
                    self.computer.state = state.get_copy()
                except:
                    pass
                continue

            else:
                if self.score > 0:
                    saves.append((self.score, self.computer.state.get_copy()))  
                    saves = saves[-200:]
                int_input = {",": -1, ".": 0, "-": 1}.get(user_input, 0)
                self.computer.add_input(int_input)
                i+= 1


def solve_part_1(machine):
    machine.computer.reset()
    machine.computer.run()
    outputs = machine.computer.state.outputs
    n_walls = sum(1 for i in islice(outputs, 2, None, 3) if i == 2)
    print(f"Part 1 answer: {n_walls}")


if __name__ == "__main__":
    logging.getLogger().setLevel("WARNING")

    raw_in = read_input('data/day_13.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    machine = ArcadeMachine(program)

    #solve_part_1(machine)

    machine.play()