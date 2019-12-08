from typing import List
import logging
from itertools import permutations

from common import read_input
from computer import Computer

logging.basicConfig(format='%(levelname)s %(message)s')


class Amp:
    def __init__(self, program, phase):
        self.phase = phase
        self.computer = Computer(program)
        self.computer.add_input(phase)
        self.computer.run()

    def __repr__(self):
        return f"Amplifier, computer state:\n{self.computer}"

    def amplify(self, in_signal):
        self.computer.add_input(in_signal)
        self.computer.run()
        return self.computer.outputs[-1]
        

def solve(program, phase_possibilities):
    phase_combos = permutations(phase_possibilities)

    all_outputs = []
    for phase_order in phase_combos:
        amps = [Amp(program, p) for p in phase_order]

        signal = 0
        iteration = 0
        while True:
            iteration += 1
            logging.info(f"Loop: {iteration}, signal value {signal}")

            for i in range(5):
                # print(f"Amp {i} running on signal {signal}")
                signal = amps[i].amplify(signal)

            if amps[4].computer.state == "FINISHED":
                all_outputs.append(signal)
                break

    return max(all_outputs)


if __name__ == "__main__":
    logging.getLogger().setLevel("WARNING")

    raw_in = read_input('data/day_7.txt')
    program = [int(i) for i in raw_in[0].split(',')]

    print("Step 1 answer: ", solve(program, [0,1,2,3,4]))
    print("Step 2 answer: ", solve(program, [5,6,7,8,9]))
