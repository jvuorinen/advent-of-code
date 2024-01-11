import logging

logging.basicConfig(format="%(levelname)s %(message)s")

from utils import read_input
from computer import Computer

if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")

    raw_in = read_input("inputs/day_09.txt")
    program = [int(i) for i in raw_in[0].split(",")]

    c = Computer()
    c.load(program)

    # Part 1
    c.reset()
    c.add_input(1)
    c.run()
    print(c.state.outputs[-1])

    # Part 2
    c.reset()
    c.add_input(2)
    c.run()
    print(c.state.outputs[-1])
