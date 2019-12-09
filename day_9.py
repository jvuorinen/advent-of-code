import logging
logging.basicConfig(format='%(levelname)s %(message)s')

from common import read_input
from computer import Computer

if __name__ == "__main__":
    logging.getLogger().setLevel('INFO')

    raw_in = read_input('data/day_9.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    c = Computer()
    c.load(program)

    # Part 1
    c.reset()
    c.add_input(1)
    c.run()


    # Part 1
    c.reset()
    c.add_input(2)
    c.run()