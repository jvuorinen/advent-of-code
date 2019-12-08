from typing import List
import logging

from common import read_input
from computer import Computer

logging.basicConfig(format='%(levelname)s %(message)s')



if __name__ == "__main__":
    logging.getLogger().setLevel("WARNING")

    raw_in = read_input('data/day_5.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    computer = Computer(program)

    # Part 1
    computer.reset()
    computer.add_input(1)
    computer.run() 
    print(f"Part 1 answer: {computer.outputs[-1]}") # Should be 9219874

    # Part 2
    computer.reset()
    computer.add_input(5)
    computer.run() 
    print(f"Part 1 answer: {computer.outputs[-1]}") # Should be 5893654
