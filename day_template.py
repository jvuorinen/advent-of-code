import logging
logging.basicConfig(format='%(levelname)s %(message)s')

from common import read_input

if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    raw_in = read_input('data/day_x.txt')