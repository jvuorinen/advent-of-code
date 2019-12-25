from typing import List
import logging

from common import read_input
from computer import Computer


def find_arguments(program, desired_value):
    logging.info(f"Finding correct parameter values to get {desired_value}")
    logging.getLogger().setLevel("WARNING")
 
    LOW, HIGH = 0, 99

    computer = Computer()
    results = {}
    for n in range(LOW, HIGH+1):
        for v in range(LOW, HIGH+1):
            computer.load(program, n, v)
            computer.run()
            res = computer.state.mem[0]
            results[res] = (n, v)

    return results.get(desired_value, "Desired result not found")


if __name__ == "__main__":
    logging.getLogger().setLevel("DEBUG")

    raw_in = read_input('data/day_2.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    # Part 1
    computer = Computer()
    computer.load(program, 12, 2)
    computer.run()
    print("Part 1 result:",  computer.state.mem[0]) # Should be 3790689

    # Part 2
    n, v = find_arguments(program, 19690720)
    print("Part 2 result:",  str(100 * n + v)) # Should be 6533

